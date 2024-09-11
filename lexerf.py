import sys

class Token:
    def __init__(self, tipo, texto, fila, columna):
        self.tipo = tipo
        self.texto = texto
        self.fila = fila
        self.columna = columna

class Lexer:
    def __init__(self, nombre_archivo):
        with open(nombre_archivo, 'r') as archivo:
            self.codigo = archivo.read()
        self.codigo += " \n"
        self.posicion = 0
        self.fila = 1
        self.columna = 1
        self.tokens = []

        self.simbolos = {
            '+': 'tk_suma',
            '-': 'tk_resta',
            '*': 'tk_multiplicacion',
            '/': 'tk_division',
            '=': 'tk_igual',
            '>': 'tk_mayorque',
            '<': 'tk_menorque',
            '==': 'tk_iguala',
            '!=': 'tk_diferente',
            '>=': 'tk_mayoroigualque',
            '<=': 'tk_menoroigualque',
            '+=': 'tk_masigual',
            '-=': 'tk_restaigual',
            '*=': 'tk_porigual',
            '/=': 'tk_divigual',
            '%': 'tk_modulo',
            '&': 'tk_andlogico',
            '|': 'tk_orlogico',
            '!': 'tk_negacionlogica',
            '~': 'tk_negacionaniveldbits',
            '^': 'tk_xorlogico',
            '<<': 'tk_despalaizquierda',
            '>>': 'tk_despaladerecha',
            '**': 'tk_exponenciacion',
            '//': 'tk_divisionentera',
            '(': 'tk_par_izq',
            ')': 'tk_par_der',
            '{': 'tk_llaveizquierda',
            '}': 'tk_llavederecha',
            '[': 'tk_corcheteizquierdo',
            ']': 'tk_corchetederecho',
            ',': 'tk_coma',
            ':': 'tk_dos_puntos',
            ';': 'tk_puntoycoma',
            '.': 'tk_punto_decimal'
        }

        self.reservadas = {
            'False': 'False',
            'print': 'print',
            'bool': 'bool',
            'None': 'None',
            'True': 'True',
            'and': 'and',
            'as': 'as',
            'range': 'range',
            'assert': 'assert',
            'async': 'async',
            'await': 'await',
            'break': 'break',
            'class': 'class',
            'continue': 'continue',
            'def': 'def',
            'del': 'del',
            'elif': 'elif',
            'else': 'else',
            'except': 'except',
            'finally': 'finally',
            'for': 'for',
            'from': 'from',
            'global': 'global',
            'if': 'if',
            'import': 'import',
            'in': 'in',
            'is': 'is',
            'lambda': 'lambda',
            'nonlocal': 'nonlocal',
            'not': 'not',
            'or': 'or',
            'pass': 'pass',
            'raise': 'raise',
            'return': 'return',
            'try': 'try',
            'while': 'while',
            'with': 'with',
            'yield': 'yield'
        }

    def get_token_type(self, texto):
        if texto in self.reservadas:
            return texto
        if texto in self.simbolos:
            return self.simbolos[texto]
        if texto.isidentifier():
            return 'id'
        if texto.isdigit():
            return 'ENTERO'
        if texto.startswith('"') and texto.endswith('"'):
            return 'tk_cadena'
        return None

    def get_next_token(self):
        token_text = ""
        estado_actual = 'INICIAL'

        while self.posicion < len(self.codigo):
            char = self.codigo[self.posicion]
            next_estado = None
            transition_found = False

            # Verificar transiciones y manejar cada estado
            if estado_actual == 'INICIAL':
                if char.isspace():
                    if char == '\n':
                        self.fila += 1
                        self.columna = 1
                    else:
                        self.columna += 1
                    self.posicion += 1
                    continue

                if char in self.simbolos:
                    token_text = char
                    tipo = self.simbolos.get(token_text, None)
                    if tipo:
                        self.tokens.append(Token(tipo, token_text, self.fila, self.columna))
                    self.posicion += 1
                    self.columna += 1
                    continue

                if char.isalpha() or char == '_':
                    estado_actual = 'IDENTIFICADOR'
                    token_text += char
                    next_estado = 'IDENTIFICADOR'
                elif char.isdigit():
                    estado_actual = 'ENTERO'
                    token_text += char
                    next_estado = 'ENTERO'
                elif char == '"':
                    estado_actual = 'CADENA'
                    token_text += char
                    next_estado = 'CADENA'
                else:
                    print(f"Error léxico en fila {self.fila}, columna {self.columna}: {char}")
                    self.posicion += 1
                    self.columna += 1
                    continue

            elif estado_actual == 'IDENTIFICADOR':
                if char.isalnum() or char == '_':
                    token_text += char
                else:
                    tipo = self.get_token_type(token_text)
                    if tipo:
                        self.tokens.append(Token(tipo, token_text, self.fila, self.columna - len(token_text)))
                    token_text = ""
                    estado_actual = 'INICIAL'
                    continue

            elif estado_actual == 'ENTERO':
                if char.isdigit():
                    token_text += char
                else:
                    tipo = self.get_token_type(token_text)
                    if tipo:
                        self.tokens.append(Token(tipo, token_text, self.fila, self.columna - len(token_text)))
                    token_text = ""
                    estado_actual = 'INICIAL'
                    continue

            elif estado_actual == 'CADENA':
                if char == '"':
                    token_text += char
                    tipo = 'tk_cadena'
                    self.tokens.append(Token(tipo, token_text, self.fila, self.columna - len(token_text)))
                    token_text = ""
                    estado_actual = 'INICIAL'
                else:
                    token_text += char

            self.posicion += 1
            self.columna += 1

        # Procesar el último token
        if token_text:
            tipo = self.get_token_type(token_text)
            if tipo:
                self.tokens.append(Token(tipo, token_text, self.fila, self.columna - len(token_text)))

        return self.tokens

def main():
    if len(sys.argv) != 3:
        print("Uso: python lexerf.py <archivo_entrada> <archivo_salida>")
        return

    nombre_archivo_entrada = sys.argv[1]
    nombre_archivo_salida = sys.argv[2]

    lexer = Lexer(nombre_archivo_entrada)
    tokens = lexer.get_next_token()

    with open(nombre_archivo_salida, "w") as archivo_salida:
        for token in tokens:
            if token.tipo == 'id':
                archivo_salida.write(f"<{token.tipo},{token.texto},{token.fila},{token.columna}>\n")
            elif token.tipo in lexer.reservadas.values() or token.tipo in lexer.simbolos.values():
                archivo_salida.write(f"<{token.tipo},{token.fila},{token.columna}>\n")
            else:
                archivo_salida.write(f"<{token.tipo},{token.fila},{token.columna}>\n")

if __name__ == "__main__":
    main()
