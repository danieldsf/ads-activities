# Games API

## Questoes:

### Pesquise qual o melhor padrão para validações extras em no DRF. Na própria view ou no serializer?

	A validacao no Serializer eh generica, enquanto a validacao na view eh especifica. Dependendo do caso, especialmente quando existe apenas uma funcao (ou um conjunto pequeno de funcoes) que necessita de uma validacao extra, a validacao na view eh interessante. De outra forma, evita-se repeticao de codigo ou validar no serializer.

### Faça as seguintes validações na API proposta:

	- [POST, PUT]: Jogos não podem ter campos vazios;
	- [POST, PUT]: Jogos não podem ter nomes repetidos;
	- [DELETE]: Somente jogos que ainda não foram lançados podem ser excluídos;

	DONE

### Que status codes você usaria? Ou usaria os mesmos? Pesquise e implemente;

	Eu usaria 409 para o DELETE caso o filme nao tivesse sido lancao ainda, uma vez que existe uma terceiro estado para uma delecao: (O dado existe, mas possui pre-requisito para ser destruido)


### Retorne também uma informação descritiva ao retornar um erro de validação.

	DONE