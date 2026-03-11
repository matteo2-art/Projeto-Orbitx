# OrbitX — Chart Data Pipeline

## Ficheiros

| Ficheiro | Função |
|---|---|
| `generate_chart_data.py` | Pipeline Python — descarrega JSR, combina dados de ataques, escreve o JSON |
| `chart_data.json` | Output consumido por `index.html` — **nunca editar manualmente** |
| `index.html` | Carrega `chart_data.json` de forma assíncrona via `fetch()` |
| `.github/workflows/update_chart_data.yml` | GitHub Action — corre automaticamente todas as semanas |

---

## Correr localmente

```bash
# Instalar dependência (só uma vez)
pip install requests

# Gerar / atualizar o JSON
python3 generate_chart_data.py
```

O ficheiro `chart_data.json` é criado (ou substituído) na mesma pasta.

---

## Configurar a automação no GitHub Pages

### Passo 1 — Criar o repositório

1. Vai a [github.com/new](https://github.com/new) e cria um repositório **público** (necessário para GitHub Pages gratuito).
2. Dá-lhe um nome, por exemplo `orbitx-website`.

### Passo 2 — Fazer upload dos ficheiros

Faz o upload de todos os ficheiros do site para a raiz (`/`) do repositório:

```
orbitx-website/
├── index.html
├── generate_chart_data.py
├── chart_data.json          ← gera este primeiro localmente
└── .github/
    └── workflows/
        └── update_chart_data.yml
```

> **Importante:** cria o `chart_data.json` localmente (`python3 generate_chart_data.py`) antes do primeiro upload, para que o gráfico apareça imediatamente.

### Passo 3 — Ativar o GitHub Pages

1. No repositório, vai a **Settings → Pages**.
2. Em **Source**, seleciona `Deploy from a branch`.
3. Escolhe o branch `main` e a pasta `/ (root)`.
4. Clica em **Save**.
5. Após ~1 minuto o site fica disponível em `https://<teu-utilizador>.github.io/orbitx-website/`.

### Passo 4 — Verificar a GitHub Action

1. Vai ao separador **Actions** do repositório.
2. Deves ver o workflow **"Update Chart Data"** listado.
3. Para testar imediatamente, clica em **"Run workflow"** → **"Run workflow"** (botão verde).
4. O workflow irá:
   - Descarregar o `stat001.txt` do JSR
   - Regenerar o `chart_data.json`
   - Fazer commit e push automático se os dados mudaram
5. A partir daí, corre **todos os domingos às 03:00 UTC** sem nenhuma intervenção.

### Passo 5 — Permissões do workflow (se o push falhar)

Se o passo de push falhar com erro de permissões:

1. Vai a **Settings → Actions → General**.
2. Em **Workflow permissions**, seleciona **"Read and write permissions"**.
3. Clica em **Save** e volta a correr o workflow.

---

## Atualizar os dados de ciberataques

Os dados de ataques são curados manualmente (relatórios PDF, Space ISAC, CSIS). Para os atualizar:

1. Edita o dicionário `CYBER_INCIDENTS` em `generate_chart_data.py`.
2. Corre `python3 generate_chart_data.py` localmente para verificar o output.
3. Faz commit dos dois ficheiros alterados (`generate_chart_data.py` + `chart_data.json`).
4. O GitHub Pages serve os novos dados automaticamente após o push.

---

## Estrutura do `chart_data.json`

```json
{
  "meta": {
    "version": "2.0",
    "generated_utc": "2025-03-11T03:00:00Z",
    "description": "...",
    "satellite_sources": [ "..." ],
    "attack_sources": [ "..." ],
    "key_caveat": "..."
  },
  "years":      [ 1957, 1960, ... ],
  "attacks":    [ 0, 0, ... ],
  "satellites": [ 1, 18, ... ]
}
```

---

## Tratamento de erros

| Situação | Comportamento |
|---|---|
| `chart_data.json` não encontrado | Mensagem de erro discreta dentro da área do gráfico; resto da página não é afetado |
| JSR indisponível durante o workflow | O script termina com `exit code 1`; o GitHub Action falha visivelmente; o JSON anterior é preservado |
| Dados corrompidos / arrays com comprimento errado | A validação interna (`validate_payload`) impede a escrita e termina com erro |