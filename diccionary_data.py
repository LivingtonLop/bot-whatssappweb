"""Listas Fijas"""


#Country Codes
COUNTRY_CODES = {
  "Argentina": "+54",
  "Bolivia": "+591",
  "Chile": "+56",
  "Colombia": "+57",
  "Costa Rica": "+506",
  "Cuba": "+53",
  "Ecuador": "+593",
  "El Salvador": "+503",
  "España": "+34",
  "Guatemala": "+502",
  "Honduras": "+504",
  "México": "+52",
  "Nicaragua": "+505",
  "Panamá": "+507",
  "Paraguay": "+595",
  "Perú": "+51",
  "Puerto Rico": "+1-787",
  "Puerto Rico2":"+1-939",
  "República Dominicana": "+1-809",
  "República Dominicana2": "+1-829",
  "República Dominicana3": "+1-849",
  "Uruguay": "+598",
  "Venezuela": "+58",
  "Guinea Ecuatorial": "+240"
}

#Lista negra [Banear al usuario/miembro y eliminar mensaje]
LIST_BLACK = [
    "facuck",
    "facu gay",
    "grupo muerto",
    "pinche grupo muerto",
    "grupo en decadencia",
    "facuncita",
    "Facuncita",
    "faculo",
    "tarao",
    "calla tarao",
    "pasen cp",
    "pedofilo",
    "porno infantil",
    "facu peruka",
    "facu dictador",
    "facu rosca",
    "facu broca"
]
#Lista gris [Solo eliminar mensaje]
LIST_GREY = [
    "causa",
    "crack",
    "mongol",
    "huevón",
    "broca",
    "chamo",
    "compa",
    "ñaño",
    "primo",
    "charapa",
    "guambra",
    "burro",
    "burra",
    "ñoño",
    "farsante",
    "hipócrita",
    "caretuco",
    "sobrado",
    "metiche",
    "jodón",
    "jodida",
    "malcriado",
    "sobrino",
    "abuelo",
    "abuela",
    "don nadie",
    "sin vida",
    "mamón",
    "mamón/a",
    "nazi",
    "neonazi",
    "fascista",
    "racista",
    "homofóbico",
    "homofóbica",
    "machista",
    "puto",
    "puta",
    "zorra",
    "imbécil",
    "maricón",
    "estúpido",
    "idiota",
    "subnormal",
    "basura humana",
    "muerete",
    "desgraciado",
    "sidoso",
    "tarado",
    "tarada",
    "degenerado",
    "degenerada",
    "pendejo",
    "pendeja",
    "chupapijas",
    "come mierda",
    "hijo de puta",
    "madre tuya",
    "padre tuyo"
]

# Lista de formatos de links que se consideran spam
LIST_LINK_SPAM = [
    "chat.whatsapp.com",
    "t.me",  # Telegram links
    "discord.gg",  # Discord invite links
    "facebook.com/groups",  # Facebook groups
    "wa.me",  # WhatsApp short links
    "bit.ly",  # Shortened links often used in spam
    "goo.gl",
    "tinyurl.com",
    "youtu.be",  # YouTube short links (sometimes used for spam)
    "instagram.com/invite",
    "linktr.ee"  # Linktree often used to promote multiple links
]

# Diccionario de países con códigos telefónicos asociados a fraudes en WhatsApp y Telegram
COUNTRY_CODES_SPAM_OR_SCAM = {
    "Pakistán": "+92",
    "Marruecos": "+212",
    "Argelia": "+213",
    "Túnez": "+216",
    "Libia": "+218",
    "Senegal": "+221",
    "Mauritania": "+222",
    "Malí": "+223",
    "Costa de Marfil": "+225",
    "Benín": "+229",
    "Liberia": "+231",
    "Ghana": "+233",
    "Nigeria": "+234",
    "Chad": "+235",
    "Camerún": "+237",
    "Seychelles": "+248",
    "Sudán": "+249",
    "Kenia": "+254",
    "Tanzania": "+255",
    "Zambia": "+260",
    "Bielorrusia": "+375",
    "Ucrania": "+380",
    "Serbia": "+381",
    "Macedonia del Norte": "+389",
    "República Checa": "+420",
    "Reino Unido (números virtuales)": "+447",
    "Hong Kong": "+852",
    "Bangladesh": "+880",
    "Maldivas": "+960",
    "Jordania": "+962",
    "Siria": "+963",
    "Kuwait": "+965",
    "Emiratos Árabes Unidos": "+971",
    "Georgia": "+995",
    "Nueva Zelanda": "+64",
    "Indonesia": "+62"  # Agregado Indonesia
}

