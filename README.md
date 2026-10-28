# 🌤️ Monitor de Clima de São Paulo

Sistema meteorológico para coleta, armazenamento e análise de dados climáticos da cidade de São Paulo ,cobrindo os últimos 90 dias de histórico e a previsão dos próximos 7 dias.

-----------------------------------------------------------------------------------------------------

## COMO O SISTEMA FUNCIONA

O projeto é dividido em dois programas independentes que conversam entre si:

1. **`Weather_service` (Backend / API):**
* Conecta na internet (Open-Meteo), baixa os dados e salva tudo localmente no banco SQLite (`weather.db`).
* Não faz médias nem cálculos: sua única função é armazenar com segurança e entregar os dados brutos.
* **Resiliência:** se a internet cair após a primeira coleta, o sistema continua funcionando com os dados locais salvos.


2. **`weather_analyzer` (Cliente CLI):**
* Interface de terminal com menu interativo de 1 a 7.
* Valida as datas digitadas e faz todas as contas matemáticas localmente em `analysis.py` (média de temperatura, total de chuva, comparativo com umidade e extremos).



---

## COMO PREPARAR E RODAR O PROJETO 

### Passo 1: Instalar as ferramentas necessárias

Abra o terminal na pasta principal do projeto (`Projeto-tempo`):

* **No Windows:**
```powershell
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt

```


* **No Mac / Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

```



> Esse comando cria o ambiente e baixa automaticamente todas as bibliotecas necessárias (`fastapi`, `uvicorn`, `requests`, `pytest`).

---

### Passo 2: Ligar o Servidor Backend (Terminal 1)

Abra o primeiro terminal na pasta do projeto:

* **No Windows:**
```powershell
cd Weather_service
.\.venv\Scripts\python.exe -m uvicorn main:app --reload

```


*(Ou com a venv ativada: `uvicorn main:app --reload`)*
* **No Mac / Linux:**
```bash
cd Weather_service
./.venv/bin/python -m uvicorn main:app --reload

```



> A API estará ativa em `[http://127.0.0.1:8000](http://127.0.0.1:8000)` (documentação interativa Swagger em `/docs`). Deixe este terminal aberto.

---

### Passo 3: Iniciar o Analisador Interativo (Terminal 2)

Abra um segundo terminal na pasta do projeto:

* **No Windows:**
```powershell
cd weather_analyzer
..\Weather_service\.venv\Scripts\python.exe cli.py

```


*(Ou com a venv ativada: `python cli.py`)*
* **No Mac / Linux:**
```bash
cd weather_analyzer
../Weather_service/.venv/bin/python cli.py

```



> **Como usar o menu no terminal:**
> 1. Digite **1** para coletar e salvar os dados no banco pela primeira vez.
> 2. Use as opções **2, 3, 4, 5 ou 6** para visualizar os relatórios e estatísticas.
> 3. Digite **7** para sair.
> 
> 

---

## 🧪 Testes Automatizados (PyTest)

Para rodar os testes de validação matemática a partir da pasta principal (`Projeto-tempo`):

* **No Windows:**
```powershell
.\Weather_service\.venv\Scripts\python.exe -m pytest tests/

```


* **No Mac / Linux:**
```bash
./Weather_service/.venv/bin/python -m pytest tests/

```



> Resultado esperado: **`4 passed`** (100% de sucesso nas checagens de médias, acumulados de chuva e listas vazias).

---

## 💬 Perguntas da Apresentação e Mentoria

### 1. Por que dividir o projeto em dois programas?

Para manter a separação de tarefas. Um programa cuida só de buscar na internet e guardar no banco com segurança (`Weather_service`). O outro cuida de interagir com o usuário e fazer as contas (`weather_analyzer`). Se um dia a interface mudar (por exemplo, virar um app visual), o banco e a coleta continuam funcionando sem precisar mexer neles.

### 2. Quem faz o quê no sistema?

* **API (`Weather_service`):** Conecta na Open-Meteo, grava no SQLite e entrega as listas de dados brutos pelas rotas HTTP.
* **Analisador (`weather_analyzer`):** Mostra o menu de opções na tela, valida se as datas estão certas e processa todas as contas de média, acumulado de chuva e extremos.

### 3. O que acontece se a Open-Meteo cair ou a internet sumir?

O sistema continua funcionando normalmente. Na primeira coleta, todos os 90 dias de histórico e os 7 dias de previsão ficam gravados localmente no arquivo `weather.db` (SQLite). Se a internet cair depois, o analisador continua gerando todos os relatórios direto desse banco local.

### 4. Se coletar várias vezes, o banco fica com dados repetidos?

Não. A data e hora de cada medição (`datetime`) é uma chave primária (`PRIMARY KEY`). O salvamento usa o comando `INSERT OR REPLACE`, que apenas atualiza as informações daquela hora se ela já existir, sem duplicar nenhuma linha.

### 5. Como você tem certeza de que os cálculos estão certos?

Foram criados testes automatizados com o framework `pytest` no arquivo `tests/test_analysis.py`. Eles usam números controlados (ex: temperaturas 10, 20 e 30) e checam se a média resulta exatamente em 20, além de validar somas de chuva e listas vazias. Todos os 4 testes foram aprovados com 100% de sucesso.

### 6. O que precisaria mudar para atender outra cidade?

Basta trocar apenas três variáveis no início do arquivo `Weather_service/clients/open_meteo_client.py`: a latitude, a longitude e o fuso horário. Todo o restante do banco, da API e do analisador funciona da mesma forma, sem alterações.

### 7. Como aceitar perguntas em linguagem natural (IA)?

Bastaria colocar uma inteligência artificial (LLM) no início do `cli.py` apenas como interpretadora de texto. Quando o usuário digitar *"qual foi o dia mais frio?"*, a IA apenas identifica o comando e chama a função Python já existente (`calcular_resumo_periodo`). A IA só traduz o pedido, enquanto todos os cálculos matemáticos continuam sendo feitos de forma determinística e precisa pelo código Python.
