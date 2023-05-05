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

## Hozzáadás discord szerverhez

1. Hozz létre egy botot itt: https://discord.com/developers/applications
2. Adj neki jogokat
3. A kapott token segítségével indísd el a botot
4. keresd meg a OATH CLIENT ID-t
5. Hívd meg a botot: https://discord.com/api/oauth2/authorize?client_id=CLIENT_ID&permissions=0&scope=bot
6. Profit!
