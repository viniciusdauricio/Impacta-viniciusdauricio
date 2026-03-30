1. Ambiente virtual
```
python -m venv env 
source env/bin/activate
## Windows
>> python -m venv env 
>> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
>> .\env\Scripts\Activate.ps1 
```

2. Requirements
```
## Para gerar o arquivo de dependências
>> pip freeze >> requirements.txt
## Para instalar os pacotes
>> pip install -r requirements.txt 
```

3. Criação do PYTHONPATH na raiz do projeto
```
>> export PYTHONPATH=$PYTHONPATH:./
## For Windows
>> $env:PYTHONPATH = "$env:PYTHONPATH;$(Get-Location)"
```
4. Execução do projeto
```
tox > evidencia.txt
```