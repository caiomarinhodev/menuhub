
# MenuHub

Hub que permitirá a um restaurante registrar seu menu de pratos.
## Instalação

Para rodar a aplicação você deverá seguir os passos abaixo.

1 - Instale as dependencias

```bash
  pip install -r requirements.txt
```

2 - Rode a criacao da database

```bash
flask db init

flask db migrate -m "Initial migration."

flask db upgrade
```

3 - Configure as variaveis de ambiente

```bash
  export FLASK_APP=app
```
```bash
  export FLASK_ENV=development
```

4 - Rode o app
```bash
  flask run
```
## Autores

- [@caiomarinhodev](https://www.github.com/caiomarinhodev)


## Contribuindo

Contribuições são sempre bem-vindas!

Veja `contribuindo.md` para saber como começar.

Por favor, siga o `código de conduta` desse projeto.


## Licença

[MIT](https://choosealicense.com/licenses/mit/)



