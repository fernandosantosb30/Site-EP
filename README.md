<div align="center">
  <img src="static/images/logo-ep.png" alt="EP Conexões & Negócios" width="150">

  <h1>EP Conexões & Negócios</h1>

  <p><strong>Conectando empresas, pessoas e oportunidades em telecomunicações.</strong></p>

  <p>Site institucional com identidade visual própria, experiência responsiva e contato integrado ao WhatsApp.</p>

  <p>
    <a href="#sobre-o-projeto">O projeto</a> ·
    <a href="#experiência-e-funcionalidades">Funcionalidades</a> ·
    <a href="#arquitetura-e-tecnologias">Tecnologias</a> ·
    <a href="#execução-local">Execução local</a>
  </p>
</div>

---

## Sobre o projeto

A **EP Conexões & Negócios** atua na intermediação de negócios em telecomunicações, com foco na compra e venda de last mile e na consultoria em projetos.

Este projeto traduz essa atuação em uma presença digital organizada: apresenta as soluções da empresa, facilita o primeiro contato comercial e oferece um espaço para profissionais interessados em fazer parte da equipe.

A proposta combina comunicação objetiva, consistência visual e uma arquitetura adequada a um site institucional. O conteúdo é acessível diretamente, e os caminhos de contato acompanham a navegação do visitante.

## Experiência e funcionalidades

- **Apresentação institucional:** informações sobre a empresa, suas soluções e sua abordagem de relacionamento com clientes.
- **Navegação responsiva:** layouts para diferentes tamanhos de tela e menu específico para dispositivos móveis.
- **Serviços conectados ao contato:** ao selecionar uma solução, o assunto correspondente é preenchido no formulário.
- **Contato pelo WhatsApp:** os dados informados são organizados em uma mensagem que o visitante pode revisar antes de enviar.
- **Página de carreiras:** apresentação das áreas de atuação e formulário de candidatura, com opção de canal externo configurável.
- **Perguntas frequentes:** respostas expansíveis para esclarecer serviços e orientar o primeiro contato.
- **Recursos de acessibilidade:** HTML semântico, rótulos nos campos, foco visível, navegação por teclado e respeito à preferência por movimento reduzido.

Os formulários preparam mensagens; não realizam envio automático, armazenamento de dados ou recebimento de arquivos. O envio é concluído pelo próprio visitante no WhatsApp.

## Identidade visual

O design preserva as cores da empresa e estabelece um padrão para tipografia, espaçamentos, cartões, botões e formulários nas duas páginas.

| Cor | Código | Aplicação |
| --- | --- | --- |
| Azul | `#042940` | Base da identidade e fundos principais |
| Azul-escuro | `#031e30` | Contraste entre seções |
| Verde-petróleo | `#055a5d` | Áreas de destaque e elementos de apoio |
| Amarelo-lima | `#DBF228` | Chamadas para ação e destaques da marca |

A hierarquia de conteúdo conduz o visitante da apresentação da empresa à escolha de uma solução e ao contato, mantendo uma linguagem visual consistente.

## Arquitetura e tecnologias

O projeto utiliza **Python e Flask** para organizar rotas e templates **Jinja2**, com uma etapa de exportação para publicação estática. O frontend utiliza **HTML, CSS e JavaScript**, sem framework de interface.

| Camada | Tecnologia | Responsabilidade |
| --- | --- | --- |
| Estrutura e templates | HTML5 e Jinja2 | Conteúdo semântico e componentes compartilhados |
| Interface | CSS3 | Identidade visual, responsividade e estados de interação |
| Interatividade | JavaScript | Menu, seleção de serviços e preparação de mensagens |
| Aplicação | Python e Flask | Rotas, configuração e renderização dos templates |
| Publicação | Build estático e configuração Render | Geração e distribuição das páginas e dos arquivos públicos |
| Testes | Python `unittest` e Node.js `node:test` | Verificação de rotas, exportação e fluxos de contato |

### Decisões de implementação

**Publicação estática.** O arquivo `build.py` gera as páginas em `dist/`. Nesse modo, a visita não depende da inicialização de um processo Flask: o servidor Python participa da geração, e o site publicado entrega arquivos estáticos.

**Templates compartilhados.** Cabeçalho, rodapé e mensagens de validação são reutilizados, facilitando a manutenção da identidade e da navegação.

**Carregamento direto.** O conteúdo não depende de uma tela intermediária ou de uma requisição JavaScript para aparecer. As fontes utilizam a pilha do sistema, o script é carregado com `defer` e imagens fora da primeira seção usam carregamento adiado.

**Contato com contexto.** O formulário reúne os dados e o serviço de interesse em uma mensagem codificada para o WhatsApp. Sem JavaScript, os links diretos de contato continuam disponíveis.

## Organização do repositório

```text
├── app.py                       # Criação e configuração da aplicação Flask
├── build.py                     # Exportação das páginas para publicação estática
├── config/                      # Configurações por variáveis de ambiente
├── routes/                      # Rotas das páginas e formulários
├── static/
│   ├── css/                     # Estilos e regras responsivas
│   ├── images/                  # Identidade visual e imagens institucionais
│   └── js/                      # Interações da interface
├── templates/                   # Templates Jinja2 das páginas e componentes
├── tests/                       # Testes Python e JavaScript
├── render.yaml                  # Configuração do Static Site no Render
└── requirements.txt             # Dependências Python
```

## Execução local

Requer **Python 3.12 ou superior**. O Node.js é opcional e utilizado apenas para executar os testes JavaScript.

```bash
git clone https://github.com/fernandosantosb30/Site-EP.git
cd Site-EP
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python build.py
python -m http.server 8000 --directory dist
```

Acesse [localhost:8000](http://localhost:8000). A página de carreiras está disponível em `/trabalhe-conosco/`.

No Windows, utilize `python` no lugar de `python3` e ative o ambiente com `.venv\Scripts\Activate.ps1`.

## Qualidade e validação

Os testes cobrem renderização das páginas, validação de campos no Flask, preservação de acentos nas mensagens, configuração do canal de candidaturas e integridade dos caminhos da exportação estática. Os testes JavaScript verificam a preparação de mensagens de contato e candidatura e a rejeição de campos obrigatórios preenchidos apenas com espaços, sem enviar dados ou abrir o WhatsApp.

```bash
python -m unittest discover -s tests -v
node --test tests/test_forms.cjs
```

## Publicação e configuração

O repositório inclui um `render.yaml` para publicação como **Static Site**. Na configuração manual, utilize:

| Campo | Valor |
| --- | --- |
| Build Command | `pip install -r requirements.txt && python build.py` |
| Publish Directory | `dist` |
| Root Directory | Raiz do repositório; deixe o campo vazio |

As páginas possuem arquivos HTML próprios. Não é necessário configurar um rewrite global para `index.html`. A pasta `dist/` é gerada durante o build e não precisa ser versionada.

Para migrar de um Web Service existente, crie o Static Site, valide o endereço temporário e depois configure o domínio personalizado. Atualizar o código do Web Service não altera seu tipo de hospedagem. Mantenha o serviço anterior até confirmar o funcionamento do novo endereço e do HTTPS.

### Variáveis opcionais

| Variável | Finalidade |
| --- | --- |
| `CANDIDATURE_URL` | Define um canal externo para receber candidaturas |
| `CANDIDATURE_EMAIL` | Exibe um endereço de e-mail como alternativa de contato |
| `SECRET_KEY` | Habilita as mensagens de sessão e validação no modo Flask; dispensável na publicação estática |

Na publicação estática, alterações nas variáveis de candidatura exigem um novo build. Sem configuração adicional, o fluxo utiliza o WhatsApp da empresa.

Para executar a aplicação Flask, configure `SECRET_KEY` no arquivo `.env` e utilize `python app.py`. Em uma implantação com servidor Python, o ponto de entrada para Gunicorn é `gunicorn app:app`.

## Contato

**EP Conexões & Negócios**

- [E-mail comercial](mailto:contato@epconexoesenegocios.com)
- [WhatsApp — (55) 9 9962-8003](https://wa.me/5555999628003)
- [Instagram — @epconexoes](https://www.instagram.com/epconexoes/)

**Desenvolvimento e portfólio:** [Fernando Santos](https://github.com/fernandosantosb30)
