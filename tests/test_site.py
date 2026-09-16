import unittest
from pathlib import Path
from urllib.parse import parse_qs, urlparse
from html.parser import HTMLParser
from unittest.mock import patch

from app import create_app
import build


class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.local = []
        self.forms = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        for key in ('href', 'src'):
            value = attrs.get(key, '')
            if value.startswith('/'):
                self.local.append(value.split('#')[0])
        if tag == 'form':
            self.forms.append(attrs)


class SiteTests(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config.update(TESTING=True, SECRET_KEY='test-only')
        self.client = self.app.test_client()

    def test_pages(self):
        for path in ('/', '/trabalhe-conosco'):
            response = self.client.get(path)
            self.assertEqual(response.status_code, 200)
            self.assertIn('EP Conexões', response.get_data(as_text=True))

    def test_contact_preserves_accents_and_interest(self):
        response = self.client.post('/contato', data={
            'nome': ' João ', 'whatsapp': '55999999999', 'email': 'teste@example.com',
            'interesse': 'Consultoria em projetos', 'mensagem': 'Conexão & expansão?'
        })
        self.assertEqual(response.status_code, 302)
        url = urlparse(response.location)
        self.assertEqual(url.netloc, 'wa.me')
        text = parse_qs(url.query)['text'][0]
        self.assertIn('João', text)
        self.assertIn('Consultoria em projetos', text)
        self.assertIn('Conexão & expansão?', text)

    def test_invalid_contact(self):
        response = self.client.post('/contato', data={}, follow_redirects=True)
        self.assertIn('Preencha todos', response.get_data(as_text=True))

    def test_career_redirect(self):
        response = self.client.post('/candidatura', data={
            'nome': 'Maria', 'email': 'teste@example.com', 'telefone': '55999999999',
            'mensagem': 'Experiência em redes'
        })
        self.assertEqual(response.status_code, 302)
        self.assertIn('Candidatura', parse_qs(urlparse(response.location).query)['text'][0])

    def test_static_export_has_no_backend_dependency(self):
        build.build()
        for file in build.OUTPUT.rglob('*.html'):
            parser = Links()
            html = file.read_text(encoding='utf-8')
            self.assertNotIn('{{', html)
            parser.feed(html)
            for link in parser.local:
                target = build.OUTPUT / link.lstrip('/')
                self.assertTrue(target.exists(), str(target))
            for form in parser.forms:
                self.assertEqual(form['action'], 'https://wa.me/5555999628003')
                self.assertEqual(form['method'], 'get')
                self.assertIn('data-whatsapp', form)

    def test_configured_career_channel(self):
        self.app.config.update(CANDIDATURE_URL='https://example.com/careers',
                               CANDIDATURE_EMAIL='careers@example.com')
        with patch.object(build, 'create_app', return_value=self.app):
            build.build()
        html = (build.OUTPUT / 'trabalhe-conosco/index.html').read_text()
        self.assertIn('https://example.com/careers', html)
        self.assertIn('mailto:careers@example.com', html)
        self.assertNotIn('data-whatsapp="career"', html)
        build.build()


if __name__ == '__main__':
    unittest.main()
