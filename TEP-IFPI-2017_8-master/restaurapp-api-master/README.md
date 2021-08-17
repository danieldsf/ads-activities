[![Build Status](https://travis-ci.com/danieldsf/restaurapp-api.svg?branch=master)](https://travis-ci.com/danieldsf/restaurapp-api)

# Restaurapp

A Restful API for meal's management system using Django Rest Framework 
with the following features:

1. The API has at least four meaninful entities related via
object relational mapping database and HATEOS pattern;

2. The API que possui partes com acesso de somente leitura e partes acessíveis apenas para
usuários autenticados. Ainda existe a diferenciação para usuários autenticados,
ou seja, pontos da API com acesso administrativo, não acessível a todos os usuários;

3. The API uses: filtering, searching, and ordering for at least two models according to the specified adopted book;

4. The API documentada com Swagger ou alguma outra sugestão da
página: http://www.django-rest-framework.org/topics/documenting-your-api/ . Com critérios de paginação e Throttling definidos (esse último com diferenciacao de usuários
autenticados de não autenticados);

5. The API implements authentication and authorization using the following schemas:

	a) [JWT (JSON Web Token)](https://jwt.io/)
	
	b) [OAuth2](https://oauth.net/2/)

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

What things you need to install the software and how to install them

```
Give examples
```

## Deployment

Add additional notes about how to deploy this on a live system

## Built With

* [Django](https://www.djangoproject.com/) - The web framework used
* [Django Rest Framework](http://www.django-rest-framework.org/) - Library that provides most common API features
* [PIP](https://pypi.org/project/pip/) - Python Libraries Dependency Management
* [PostgreSQL](https://www.postgresql.org/) - Relational Database used

## Authors

* **Daniel Farias** - *Initial work* - [DanielDSF](https://github.com/PurpleBooth)
* **Kairo Costa** - *Initial work* - [KairoDEV](https://github.com/PurpleBooth)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
