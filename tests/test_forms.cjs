// Run with node --test tests/test_forms.cjs. No messages or network requests are sent.
const { test } = require('node:test');
const assert = require('node:assert/strict');
const { readFileSync } = require('node:fs');
const { runInNewContext } = require('node:vm');
const source = readFileSync(new URL('../static/js/main.js', `file://${__filename}`), 'utf8');

function submit(kind, values) {
    let destination;
    let handler;
    const fields = Object.entries(values).map(([name, value]) => ({ name, value }));
    const form = {
        dataset: { whatsapp: kind },
        addEventListener: (_, callback) => { handler = callback; },
        querySelectorAll: () => fields,
        reportValidity: () => fields.filter(field => field.name !== 'interesse').every(field => field.value.length > 0),
    };
    runInNewContext(source, {
        document: {
            documentElement: { classList: { add() {} } },
            querySelector: () => null,
            querySelectorAll: selector => selector === 'form[data-whatsapp]' ? [form] : [],
            addEventListener() {},
        },
        window: {
            matchMedia: () => ({ addEventListener() {} }),
            location: { assign: url => { destination = url; } },
        },
        FormData: class { get(name) { return fields.find(field => field.name === name)?.value ?? null; } },
        encodeURIComponent,
    });
    handler({ preventDefault() {} });
    return destination;
}

test('static contact prepares complete, correctly encoded WhatsApp message', () => {
    const url = new URL(submit('contact', { nome: ' João ', whatsapp: '55999999999',
        email: 'teste@example.com', interesse: 'Compra e venda de last mile', mensagem: 'Conexão & expansão?\nNova linha' }));
    assert.equal(url.origin, 'https://wa.me');
    assert.equal(url.pathname, '/5555999628003');
    const text = url.searchParams.get('text');
    assert.match(text, /Nome: João\n/);
    assert.match(text, /Interesse: Compra e venda de last mile/);
    assert.ok(text.endsWith('Conexão & expansão?\nNova linha'));
});
test('static career uses the phone field and identifies the application', () => {
    const text = new URL(submit('career', { nome: 'Maria', telefone: '55988888888', email: 'teste@example.com', mensagem: 'Experiência em redes' })).searchParams.get('text');
    assert.match(text, /^Candidatura — Trabalhe Conosco/);
    assert.match(text, /WhatsApp: 55988888888/);
    assert.ok(!text.includes('null'));
});
test('whitespace-only required data does not navigate', () => {
    assert.equal(submit('contact', { nome: '   ', whatsapp: '55999999999', email: 'teste@example.com', mensagem: 'Olá' }), undefined);
});
