import pytest
from hamcrest import *


def test_plugin_has_fixture_get_graphql_schema(get_graphql_schema):
    assert_that(get_graphql_schema, not_none())


def test_plugin_has_fixture_get_graphql_obj_schema(get_graphql_obj_schema):
    assert_that(get_graphql_obj_schema, not_none())


@pytest.mark.parametrize("host, path, headers", [
    ("https://graphql.anilist.co", "/", {})
])
def test_get_schema(get_graphql_schema, host, path, headers):
    schema = get_graphql_schema(host, headers, path=path)
    assert_that(schema, is_(list))


@pytest.mark.parametrize("host, path, headers, obj_name", [
    ("https://graphql.anilist.co", "/", {}, "Page"),
    ("https://graphql.anilist.co", "/", {}, "Media"),
])
def test_get_schema(get_graphql_obj_schema, host, path, headers, obj_name):
    schema = get_graphql_obj_schema(host, headers, obj_name, path=path)

    assert_that(schema,        is_(dict))
    assert_that(schema.keys(), contains_inanyorder("kind", "name", "fields"))

    assert_that(schema["name"],   equal_to(obj_name))
    assert_that(schema["fields"], is_(list))

    for field in schema["fields"]:
        assert_that(field,         is_(dict))
        assert_that(field.keys(),  contains_inanyorder("name", "args", "isDeprecated", "type"))

        assert_that(field["args"], is_(list))
        for arg in field["args"]:
            assert_that(arg,        is_(dict))
            assert_that(arg.keys(), contains_inanyorder("defaultValue", "name", "type"))

            assert_that(arg["type"],         is_(dict))
            assert_that(arg["type"].keys(),  contains_inanyorder("name", "kind"))

        assert_that(field["isDeprecated"], is_(bool))

        assert_that(field["type"],         is_(dict))
        assert_that(field["type"].keys(), contains_inanyorder("name", "kind"))
