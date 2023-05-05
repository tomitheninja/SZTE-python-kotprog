# WeedShop anoním piac

Egy Discord bot amely teljes anonimitást biztosítva köt össze megkérdőjelezhető termékeket árusítókat érdeklődő vevőkkel.

## Telepítés:

Szükséges Python verzió: 3.10

```
pip install git+https://github.com/tomitheninja/SZTE-python-kotprog.git
```

### `config.json` fájl

Például:
```JSON
{
    "dc_token": "YOUR_BOT_TOKEN",
    "pickle": "data.pickle",
    "prefix": "!"
}
```

- `dc_token`: a Discord Bot API kulcs
- `pickle`: az adattároláshoz használt pickle fájl elérési útvonala
- `prefix`: ha nem `/` csak parancsokat akar használni, akkor ezzel a prefixxel kell kezdeni a parancsokat `/` helyett

## Futtatás
```
python3 -m szte_python_kotprog [konfigurációs fájl]
```

Ha üresen marad a konfigurációs fájl helye, akkor alapból `config.json`-t fog keresni
