## Arquitetura de Extração de Dados: Padrões e Princípios

Este documento descreve a aplicação dos **princípios SOLID** e dos **Design Patterns** (Factory, Strategy, Repository e Facade) na solução de extração de dados implementada em `src/`. A união dessas abordagens promove um código **modular**, **testável**, **extensível** e **de fácil manutenção**.

---

### 1. Princípios SOLID

1. **Single Responsibility Principle (SRP)**

   * Cada classe tem uma única responsabilidade. Ex: `InmetExtractionS` lida apenas com a extração INMET; `LocalRepository` cuida apenas do caminho de onde salvar.

2. **Open/Closed Principle (OCP)**

   * Classes estão abertas para extensão, mas fechadas para modificação. Para suportar novas fontes, basta criar novas `Strategy` e registrá-las em `mapping_strategy_extraction.py`, sem alterar fábrica ou fachada.

3. **Liskov Substitution Principle (LSP)**

   * As implementações de interfaces (`ExtractionSI`, `RepositoryI`, `FactoryI`) podem ser substituídas sem quebrar o comportamento esperado.

4. **Interface Segregation Principle (ISP)**

   * Interfaces pequenas e focadas: `ExtractionSI` só declara `extract_data()`, `FactoryI` só `create()`, `RepositoryI` só acesso a caminho (get/set).

5. **Dependency Inversion Principle (DIP)**

   * Módulos de alto nível (ex.: `ExtractionFacade`) não dependem de implementações concretas, mas de **abstrações** (`FactoryI`, `RepositoryI`, `ExtractionSI`).

---

### 2. Design Patterns Empregados

| Padrão         | Objetivo principal                                    | Papel na solução                                                                                   |
| -------------- | ----------------------------------------------------- | -------------------------------------------------------------------------------------------------- |
| **Factory**    | Criar objetos sem expor lógica de instância           | `ExtractorFactory` injeta `repository` e parâmetros dinâmicos, devolvendo `ExtractionSI` corretos. |
| **Strategy**   | Encapsular algoritmos/variantes de comportamento      | Cada `ExtractionSI` (ex.: `InmetExtractionS`) implementa `extract_data()` de forma específica.     |
| **Repository** | Abstrair acesso ao armazenamento                      | `LocalRepository` implementa `RepositoryI`, desacoplando local do código de extração.              |
| **Facade**     | Oferecer interface simples para subsistemas complexos | `ExtractionFacade` orquestra fábrica, repositório e paralelismo, simplificando o `main.py`.        |

---

### 3. Fluxo de Execução Unificado

1. **Main** (`main.py`):

   * Apenas monta a `Facade` e chama `run()`.

2. **Facade** (`ExtractionFacade`):

   * Recebe `app_settings`, a fábrica e a classe de repositório.
   * Gera instâncias de repositório & strategy via `FactoryI`.
   * Executa todos em paralelo usando `multiprocessing.Pool`.

3. **Factory** (`ExtractorFactory` implementa `FactoryI`):

   * Usa `mapping_strategy_extraction.py` para resolver nome → classe.
   * Cria a `Strategy`, injetando o `RepositoryI` e os parâmetros válidos (`url`, `cities`, etc.).

4. **Strategy** (`ExtractionSI` e implementações):

   * Cada `extract_data()` baixa, filtra e salva apenas o que interessa, usando o `RepositoryI`.

5. **Repository** (`RepositoryI` e `LocalRepository`):

   * Abstrai como e onde os arquivos resultantes são armazenados.

---

### 4. Benefícios da Integração

* **Baixo acoplamento**: Alterações em como/onde armazenar não afetam Strategy ou Facade.
* **Alta coesão**: Cada classe faz apenas uma coisa.
* **Extensibilidade fácil**: Para adicionar nova fonte, basta:

  1. Criar uma nova classe `NovaExtractionS(ExtractionSI)`.
  2. Registrar em `STRATETEGY_EXTRACTION_MAPPING`.
  3. Adicionar configuração em `SETTINGS`.
* **Testabilidade**: Interfaces permitem mocks/stubs para unit tests de fábricas, strategies e fachada.
* **Manutenção simplificada**: Código organizado em camadas e responsabilidades claras.

---

### 5. Conclusão

A combinação de SOLID + Factory + Strategy + Repository + Facade permite uma arquitetura robusta, onde:

* **DIP** garante dependência apenas de abstrações.
* **OCP** mantém o sistema fácil de evoluir.
* **SRP** e **ISP** promovem clareza e simplicidade.
* **Factory** e **Strategy** oferecem flexibilidade em algoritmos.
* **Repository** isola detalhes de persistência.
* **Facade** fornece uma interface de alto nível limpa para o orquestrador.

Isso resulta em um `main.py` praticamente vazio de lógica interna, com toda a complexidade delegada a componentes bem-definidos e desacoplados.

---

## 6. Como Rodar

1. **Criar ambiente virtual** (Python 3.10 ou superior):

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate    # Linux/macOS
   .venv\Scripts\activate   # Windows
   ```

2. **Instalar dependências**:

   ```bash
   pip install -r requirements.txt
   ```

3. **Executar o script principal**:

   ```bash
   python src/main.py
   ```

Pronto! A extração será disparada conforme as configurações em `config/settings.py` e os mapeamentos de estratégia.

---

## 7. Tutorial: Como Configurar uma Nova Strategy

Para adicionar suporte a uma nova fonte de dados, siga os passos abaixo:

1. **Criar a classe da Strategy**

   * No diretório `src/strategies/extraction/`, crie um novo arquivo, por exemplo `my_source_extraction_strategy.py`.
   * Implemente a interface `ExtractionSI` e defina o método `extract_data()` com a lógica específica:

     ```python
     from interfaces.extraction_strategy_interface import ExtractionSI
     from interfaces.repository_interface import RepositoryI

     class MySourceExtractionS(ExtractionSI):
         def __init__(self, repository: RepositoryI, api_key: str, param_x: int):
             self.repository = repository
             self.api_key = api_key
             self.param_x = param_x

         def extract_data(self) -> None:
             # ex: chamar API, processar resposta e salvar arquivos
             data = fetch_from_api(self.api_key, self.param_x)
             self.repository.save(data)
     ```

2. **Registrar a Strategy no mapeamento**

   * Abra `src/config/mapping_strategy_extraction.py` e adicione sua nova classe ao dicionário:

     ```python
     from strategies.extraction.my_source_extraction_strategy import MySourceExtractionS

     STRATETEGY_EXTRACTION_MAPPING = {
         # já existentes...
         "inmet": InmetExtractionS,

         # novo mapeamento:
         "my_source": MySourceExtractionS,
     }
     ```

3. **Configurar o `SETTINGS`**

   * No arquivo `src/config/settings.py`, adicione uma seção para seu `site_name` dentro de `SETTINGS["app"]`:

     ```python
     SETTINGS = {
         "app": {
             # existente...
             "inmet": { ... },

             # nova fonte:
             "my_source": {
                 "strategy": {
                     "api_key": "SUA_CHAVE_AQUI",
                     "param_x": 42,
                 },
                 "repository": {
                     "path": "data/my_source",
                 },
             },
         }
     }
     ```

4. **Rodar a aplicação**

   * Após essas configurações, basta executar:

     ```bash
     python src/main.py
     ```
   * A `ExtractionFacade` irá reconhecer automaticamente seu novo `"my_source"`, instanciar a `MySourceExtractionS` e executar o `extract_data()` em paralelo.

---

Agora sua aplicação suporta facilmente novas fontes, sem modificar o `main.py` ou as classes de fábrica/fachada.
