# OrbitX — Chart Data Pipeline

## Ficheiros

| Ficheiro | Função |
|---|---|
| `generate_chart_data.py` | Pipeline Python — descarrega JSR, combina dados de ataques, escreve o JSON |
| `chart_data.json` | Output consumido por `index.html` — **nunca editar manualmente** |
| `index.html` | Carrega `chart_data.json` de forma assíncrona via `fetch()` |

---

## Correr o pipeline

```bash
# Instalar dependência (só uma vez)
pip install requests

# Gerar / atualizar o JSON
python3 generate_chart_data.py
```

O ficheiro `chart_data.json` é criado (ou substituído) na mesma pasta. Coloca-o no mesmo diretório que o `index.html` antes de abrir o site.

---

## Atualizar os dados de ciberataques

Os dados de ataques são curados manualmente (relatórios PDF, Space ISAC, CSIS). Para os atualizar:

1. Edita o dicionário `CYBER_INCIDENTS` em `generate_chart_data.py`.
2. Corre `python3 generate_chart_data.py` para regenerar o `chart_data.json`.
3. Substitui o `chart_data.json` antigo pelo novo.

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
| JSR indisponível | O script termina com `exit code 1` e imprime o erro; o JSON anterior é preservado |
| Dados corrompidos / arrays com comprimento errado | A validação interna (`validate_payload`) impede a escrita e termina com erro |