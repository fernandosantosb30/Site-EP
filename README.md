# EP Conexões & Negócios

Site institucional com identidade em azul (#042940), verde-petróleo (#055a5d) e amarelo-lima (#dbf228). Layout responsivo, navegação por teclado, FAQ expansível e formulários que preparam mensagens no WhatsApp.

## Por que aparecia a tela do Render?

Não há um preloader no código original. O sintoma descrito é compatível com o cold start de um **Web Service gratuito**: o Render suspende esse serviço após inatividade e precisa iniciá-lo na próxima visita. Isso acontece antes de o HTML chegar ao navegador e não pode ser eliminado com CSS ou JavaScript.

A publicação recomendada agora é **Static Site**. O Python gera as páginas apenas no build; os visitantes recebem HTML, CSS, JavaScript e imagens pela CDN, sem aguardar um servidor Flask. Os formulários continuam preparando as mensagens para revisão e envio no WhatsApp, sem depender do servidor.

Documentação: https://render.com/docs/free e https://render.com/docs/static-sites

## Executar localmente

Requer Python 3.12 ou superior.

```sh
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python build.py
python -m http.server 8000 --directory dist
```

No Windows, ative o ambiente com `.venv\Scripts\Activate.ps1` e use `python` no lugar de `python3`.

Acesse http://localhost:8000. A página de carreiras está em `/trabalhe-conosco/` e suporta acesso direto.

## Publicar no Render sem cold start

O arquivo `render.yaml` configura um novo Static Site. Também é possível configurá-lo manualmente:

1. Envie o projeto atualizado ao repositório conectado ao Render.
2. No Render, selecione **New → Static Site** e conecte esse repositório.
3. Use o Build Command `pip install -r requirements.txt && python build.py`.
4. Use o Publish Directory `dist`.
5. Verifique as duas páginas, links, menu no celular e formulários no endereço temporário do novo Static Site.
6. Migre o domínio personalizado para o Static Site em Settings → Custom Domains e aplique os registros DNS indicados pelo Render. Confirme HTTPS e o funcionamento no domínio público antes de desativar o Web Service antigo.

Somente atualizar os arquivos do Web Service existente **não** muda o tipo de hospedagem nem elimina a suspensão. O endereço `onrender.com` do serviço antigo também não é automaticamente transferido para o novo site. A publicação e a migração do domínio precisam ser feitas na conta do Render; este projeto não as executa sozinho.

Não configure um rewrite global para `index.html`: há páginas HTML reais para cada endereço. O blueprint inclui redirecionamento de `/trabalhe-conosco` para `/trabalhe-conosco/`.

## Candidaturas e contato

- `CANDIDATURE_URL` (opcional): endereço de um canal externo de candidaturas.
- `CANDIDATURE_EMAIL` (opcional): e-mail exibido como alternativa clicável.
- Configure essas variáveis no ambiente de build do Static Site e faça novo deploy quando mudarem. Sem elas, a candidatura é preparada no WhatsApp.
- Nenhum formulário envia mensagens automaticamente, armazena dados ou recebe currículos. O usuário revisa e envia pelo WhatsApp.
- Sem JavaScript, o conteúdo e a navegação permanecem disponíveis, e os links diretos do WhatsApp permitem contato. A montagem automática da mensagem na versão estática exige JavaScript.

## Flask (opcional)

O backend foi preservado. Para executá-lo, configure `SECRET_KEY` no `.env` (necessária para mensagens de validação) e rode `python app.py`. Em produção com Flask, use `gunicorn app:app` e um serviço que não suspenda se quiser evitar cold starts. A publicação estática não precisa de `SECRET_KEY`.

## Validação

```sh
python -m unittest discover -s tests -v
node --test tests/test_forms.cjs
python build.py
```

Os testes verificam páginas, validação de formulário no Flask, codificação das mensagens, canal alternativo de candidatura e integridade dos caminhos na exportação estática. Os testes JavaScript (Node.js opcional) verificam a preparação das mensagens de contato e candidatura sem abrir WhatsApp nem enviar dados. `dist/` é gerado e não precisa ser versionado.
