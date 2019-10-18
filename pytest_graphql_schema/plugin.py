import pytest
import requests


@pytest.fixture(scope="session")
def get_graphql_schema():
    query_format = """
        query IntrospectionQuery {
            __schema {
                queryType { name }
                mutationType { name }
                subscriptionType { name }
                types {
                    ...FullType
                }
                directives {
                    name
                    description
                    locations
                    args {
                        ...InputValue
                    }
                }
            }
        }

        fragment FullType on __Type {
            kind
            name
            description
            fields(includeDeprecated: {field_include_deprecated}) {
                name
                description
                args { ...InputValue }
                type { ...TypeRef }
                isDeprecated
                deprecationReason
            }
            inputFields { ...InputValue }
            interfaces { ...TypeRef }
            enumValues(includeDeprecated: {enum_include_deprecated}) {
                name
                description
                isDeprecated
                deprecationReason
            }
            possibleTypes { ...TypeRef }
        }

        fragment InputValue on __InputValue {
            name
            description
            type { ...TypeRef }
            defaultValue
        }

      fragment TypeRef on __Type {level_of_types}
    """

    def _func(host, headers, path="/graphql", field_include_deprecated=True, enum_include_deprecated=True, level=8):
        query = query_format.replace("{field_include_deprecated}", str(field_include_deprecated).lower())\
                            .replace("{enum_include_deprecated}", str(enum_include_deprecated).lower())\
                            .replace("{level_of_types}", get_level_of_types(level))

        resp = requests.post(host + path, json={"query": query}, headers=headers)
        assert resp.status_code == 200
        resp_json = resp.json()

        return resp_json["data"]["__schema"]["types"]
    return _func


@pytest.fixture(scope="session")
def get_graphql_obj_schema():
    query_format = """
        query IntrospectionQuery {
            __type(name: "{name}") {
                kind
                name
                fields {
                    name
                    args {
                        name
                        defaultValue
                        type {
                            kind
                            name
                        }
                    }
                    isDeprecated
                    type {
                        kind
                        name
                    }
                }
            }
        }
    """

    def _func(host, headers, name, path="/graphql"):
        query = query_format.replace("{name}", name)

        resp = requests.post(host + path, json={"query": query}, headers=headers)
        assert resp.status_code == 200
        resp_json = resp.json()

        return resp_json["data"]["__type"]
    return _func


def get_level_of_types(level):
    assert level > 0

    def _func(cur_level):
        if cur_level == 1:
            return [
                "    kind",
                "    name",
            ]
        return [
            "    kind",
            "    name",
            "    ofType {",
        ] + ["    " + x for x in _func(cur_level - 1)] + [
            "    }"
        ]

    return "\n".join(["{"] + _func(level) + ["}"])
