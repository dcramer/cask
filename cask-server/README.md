# cask-server


## Install

```shell
$ brew install postgresql postgis
$ pipenv sync
$ psql -c 'create extension postgis;' -U postgres
$ createdb -E utf-8 cask
$ pipenv run python manage.py migrate
$ pipenv run python manage.py runserver
```

## API

The API is a GraphQL implementation powered by Graphene. The endpoint is ``/graphql/``.

Authentication is done via the following:

1. Perform a login mutation:

```graphql
mutation{
  login(email:"foo@example.com", password:"bar"){
    errors
    ok
    token,
    user {id, email, name}
  }
}
```

2. Capture the token in the response and send it with future requests:

```http
Authorization: Token {value}
```

Here's a helpful app which lets you bind an auth header:

https://github.com/skevy/graphiql-app
