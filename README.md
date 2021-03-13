# 2021-1-JD-Eq1
Projeto da aula de desenvolvimento de jogos e entreterimento digital - Auto gerado text adventure


## Ambiente de desenvolvimento

### Ambiente virtual:

Dentro da pasta `/bin`, tem-se um conjunto de scripts para ativação do ambiente
virtual:

- `bash`/`zsh`: `$ source <venv>/bin/activate`
- `fish`: `$ source <venv>/bin/activate.fish`
- `csh`/`tcsh`: `$ source <venv>/bin/activate.csh`
- `PowerShell Core`: `$ <venv>/bin/Activate.ps1`
- `cmd.exe`: `C:\> <venv>\Scripts\activate.bat`
- `PowerShell`: `PS C:\> <venv>\Scripts\Activate.ps1`

Uma vez ativado o ambiente, é possível desativar o mesmo com o comando
`deactivate`.

Para mais informações, pode ser verificada a documentação da biblioteca de
virtualização do python:

https://docs.python.org/pt-br/3/library/venv.html

### Comandos:

Foi inserido, para o desenvolvimento dentro de um ambiente Linux, o arquivo
`makefile`. Nele um conjunto de comandos úteis para o desenvolvimento:
- `depend`I instalação das dependências. `python -m pip install -r requirements_dev.txt`.
- `test`: Execução dos testes unitários. `python -m pytest`.

A execução desses comandos deve ser feita dentro da pasta do repositório, com o
ambiente virtual ativada.
