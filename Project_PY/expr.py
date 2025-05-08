#Tommaso Mingrone [SM3201286]

class EmptyStackException(Exception):
    # Eccezione personalizzata per gestire errori di stack vuoto
    pass


class MissingVariableException(Exception):
    # Eccezione per segnalare l'assenza di una variabile nell'ambiente
    pass


class InvalidExpressionException(Exception):
    # Eccezione per espressioni invalide o non correttamente formattate
    pass


class DivisionByZeroException(ZeroDivisionError):
    # Eccezione per errori di divisione per zero nelle espressioni
    pass


class InvalidArithmeticOperationException(Exception):
    # Eccezione per operazioni aritmetiche non valide o non definite
    pass


class ArrayIndexOutOfBoundsException(IndexError):
    # Eccezione per errori relativi agli indici fuori dai limiti in un array
    pass


class VariableNotFoundException(Exception):
    # Eccezione per variabili non trovate nell'ambiente di esecuzione
    pass


class FunctionNotFoundException(Exception):
    # Eccezione per funzioni o subroutine non trovate
    pass


class InvalidArgumentError(Exception):
    # Eccezione per argomenti non validi
    pass


class EvaluateMethodNotImplemented(Exception):
    # Eccezione per il metodo evaluate non implementato nelle sottoclassi di Expression
    pass


class Stack:
    # Classe per implementare uno stack con operazioni di base

    def __init__(self):
        # Inizializza uno stack vuoto
        self.data = []

    # Metodo per aggiungere un elemento allo stack
    def push(self, x):
        self.data.append(x)

    # Metodo per rimuovere e restituire l'elemento in cima allo stack
    def pop(self):
        if self.data == []:
            raise EmptyStackException
        res = self.data[-1]
        self.data = self.data[:-1]
        return res
    
    # Metodo per verificare la lunghezza dello stack
    def size(self):
        return len(self.data)

    # Rappresentazione stringa dello stack per il debug
    def __str__(self):
        return " ".join([str(s) for s in self.data])


class Expression:
    # Classe base per le espressioni

    def __init__(self):
        # Previene l'istanziazione diretta di questa classe
        raise EvaluateMethodNotImplemented("Non è consentita l'istanziazione diretta della classe Expression. Utilizzare le sottoclassi.")

    
    @classmethod
    def from_program(cls, text, dispatch):
        """
        Metodo di classe per trasformare una stringa di testo in un oggetto Expression.
        Questo metodo è fondamentale per interpretare la notazione polacca inversa,
        creando un albero di espressioni corrispondente alla stringa di input.
        
        Args:
            text (str): La stringa di testo che rappresenta l'espressione in notazione polacca inversa.
            dispatch (dict): Un dizionario che mappa le stringhe (simboli delle operazioni) 
                            alle rispettive classi di operazioni.
        Return:
            Expression: Un oggetto Expression che rappresenta l'albero dell'espressione costruito.
        """

        stack = Stack()  # Inizializza uno stack vuoto per processare l'espressione

        for token in text.split():
            # Itera su ogni token nella stringa di input

            if token.isdigit():
                # Se il token è un numero, crea un oggetto Constant e aggiungilo allo stack
                stack.push(Constant(int(token)))

            elif token in dispatch:
                # Se il token è un operatore (presente in dispatch), procedi alla creazione dell'operazione
                arity = dispatch[token].arity
                # Controllo sull'arity per garantire il numero corretto di argomenti per l'operatore
                if arity > 0:
                    if stack.size() < arity:
                        raise ValueError(f"Numero insufficiente di argomenti per {token}")
                    # Prendi gli ultimi 'arity' elementi dallo stack e invertirli (perché siamo in notazione polacca inversa)
                    args = [stack.pop() for _ in range(arity)][::-1]
                    # Se gli argomenti sono variabili, sostituisci con i loro nomi
                    args = [arg.name if isinstance(arg, Variable) else arg for arg in args]
                    # Crea l'operazione corrispondente e aggiungila allo stack
                    operation = dispatch[token](args)
                else:
                    # Per operatori senza argomenti (arity = 0)
                    operation = dispatch[token]()
                stack.push(operation)

            else:
                # Se il token è una variabile, crea un oggetto Variable e aggiungilo allo stack
                stack.push(Variable(token))

        if stack.size() != 1:
            # Alla fine dell'elaborazione, dovrebbe rimanere un solo elemento nello stack (l'albero dell'espressione completo)
            # Altrimenti, la stringa di input non è una espressione valida
            raise ValueError("Espressione non valida")

        return stack.pop()  # Ritorna l'albero dell'espressione costruito

    # Metodo astratto per valutare l'espressione
    def evaluate(self, env):
        raise EvaluateMethodNotImplemented("Il metodo evaluate deve essere implementato dalle sottoclassi di Expression")


class Variable(Expression):
# Classe per rappresentare le variabili
    
    def __init__(self, name):
        self.name = name

    # Valuta la variabile nell'ambiente dato
    def evaluate(self, env):
        if self.name not in env:
            raise MissingVariableException(f"Valore mancante per la variabile '{self.name}'")
        return env[self.name]

    # Rappresentazione stringa della variabile
    def __str__(self):
        return self.name


class Constant(Expression):
    # Classe per rappresentare le costanti

    def __init__(self, value):
        self.value = value

    # Restituisce il valore della costante
    def evaluate(self, env):
        return self.value

    # Rappresentazione stringa della costante
    def __str__(self):
        return str(self.value)


class Operation(Expression):
    # Classe base per le operazioni

    def __init__(self, args):

        # Verifica che ogni argomento sia un'istanza valida di Expression, stringa, intero o float
        if not all(isinstance(arg, (Expression, str, int, float)) for arg in args):
            raise InvalidArgumentError("Tutti gli argomenti devono essere espressioni, variabili o valori costanti")
        self.args = args

    # Valuta l'operazione nell'ambiente dato
    def evaluate(self, env):
        evaluated_args = [] # Inizializza una lista vuota
        for arg in self.args: 
            if isinstance(arg, Expression): # Se l'argomento è un'espressione, lo valuta ricorsivamente e aggiunge il risultato alla lista
                evaluated_args.append(arg.evaluate(env))
            elif isinstance(arg, str): # Se l'argomento è una stringa (nome di una variabile), cerca il suo valore nell'ambiente e lo aggiunge alla lista
                if arg in env: # Se l'argomento è una stringa (nome di una variabile), cerca il suo valore nell'ambiente, se presente lo aggiunge
                    evaluated_args.append(env[arg])
                else:
                    raise MissingVariableException(f"Valore mancante per la variabile '{arg}'")
            else:
                evaluated_args.append(arg)
        result = self.op(*evaluated_args)
        return result


class Alloc(Expression):
# La classe Alloc inizializza una variabile con valore 0 nell'ambiente di esecuzione
    
    arity = 1

    def __init__(self, args):
        self.var_name = args[0]

    def evaluate(self, env):
        env[self.var_name] = 0
        return None

    def __str__(self):
        return f"alloc({self.var_name})"


class Valloc(Expression):
# Valloc alloca un array di dimensione specificata e lo inizializza a zero nell'ambiente
    
    arity = 2

    def __init__(self, args):
        self.size_expr = args[0]
        self.var_name = args[1]
    
    def evaluate(self, env):

        size = self.size_expr.evaluate(env)

        if not isinstance(size, int) or size < 0:
            raise InvalidArithmeticOperationException("La dimensione dell'array deve essere un intero non negativo")
        
        var_name = str(self.var_name)
        env[var_name] = [0] * size  #Inizializza l'array a 0

        return None

    def __str__(self):
        return f"valloc({self.size_expr}, {self.var_name})"

    
class Setq(Expression):
    # Setq assegna un nuovo valore a una variabile esistente nell'ambiente

    arity = 2

    def __init__(self, args):
        self.expr = args[0]         # L'espressione il cui risultato verrà assegnato alla variabile
        self.var_name = args[1]     # Il nome della variabile da aggiornare

    def evaluate(self, env):
        new_value = self.expr.evaluate(env) if isinstance(self.expr, Expression) else self.expr
        env[self.var_name] = new_value # Assegna il nuovo valore
        return new_value

    def __str__(self):
        return f"setq({self.expr}, {self.var_name})"


class Setv(Expression):
    # Setv assegna un valore a un elemento specifico di un array nell'ambiente

    arity = 3

    def __init__(self, args):
        self.expr = args[0]         # L'espressione il cui risultato verrà assegnato all'array
        self.index = args[1]        # L'indice dell'array dove assegnare il valore
        self.var_name = args[2]     # Il nome dell'array in cui assegnare il valore

    def evaluate(self, env):
        value_to_set = self.expr.evaluate(env)

        # Gestisci index come espressione, nome di variabile o valore costante
        if isinstance(self.index, Expression):
            index = self.index.evaluate(env)
        elif isinstance(self.index, str):
            if self.index in env:
                index = env[self.index]
            else:
                raise MissingVariableException(f"Valore mancante per la variabile '{self.index}'")
        else:
            index = self.index  # Se è un valore costante

        if not isinstance(index, int) or index < 0:
            raise InvalidArithmeticOperationException("L'indice deve essere un intero non negativo")

        var_name = str(self.var_name)
        if var_name not in env or not isinstance(env[var_name], list):
            raise VariableNotFoundException("La variabile specificata non esiste o non è un array")

        if index >= len(env[var_name]):
            raise ArrayIndexOutOfBoundsException("Indice fuori dai limiti dell'array")

        # Imposta il valore all'indice specificato di var_name in env
        env[var_name][index] = value_to_set
        return value_to_set

    def __str__(self):
        return f"setv({self.expr}, {self.index}, {self.var_name})"


    
class Prog2(Expression):
 # Prog2 esegue due espressioni e restituisce il risultato della prima
    
    arity = 2
    
    def __init__(self, args):
        self.expr1 = args[0]
        self.expr2 = args[1]

    def evaluate(self, env):
        
        # Valuta la seconda espressione
        self.expr2.evaluate(env)
        # Valuta la prima espressione e memorizza il suo risultato
        result = self.expr1.evaluate(env)
        # Ritorna il risultato memorizzato
        return result
    
    def __str__(self):
        return f"prog2 ({self.expr1}, {self.expr2})"


class Prog3(Expression):
# Prog3 esegue tre espressioni e restituisce il risultato della prima

    arity = 3
    
    def __init__(self, args):
        self.expr1 = args[0]
        self.expr2 = args[1]
        self.expr3 = args[2]

    def evaluate(self, env):

        # Valuta la terza espressione
        self.expr3.evaluate(env)
        # Valuta la seconda espressione 
        self.expr2.evaluate(env)
        # Valuta la prima espressione e memorizza il suo risultato
        result = self.expr1.evaluate(env)
        # Ritorna il risultato memorizzato
        return result
    
    def __str__(self):
        return f"prog3 ({self.expr1}, {self.expr2}, {self.expr3})"

    
class Prog4(Expression):
# Prog4 esegue quattro espressioni e restituisce il risultato della prima

    arity = 4
    
    def __init__(self, args):
        self.expr1 = args[0]
        self.expr2 = args[1]
        self.expr3 = args[2]
        self.expr4 = args[3]

    def evaluate(self, env):

        # Valuta la quarta espressione 
        self.expr4.evaluate(env)
        # Valuta la terza espressione 
        self.expr3.evaluate(env)
        # Valuta la seconda espressione 
        self.expr2.evaluate(env)
        # Valuta la prima espressione e memorizza il suo risultato
        result = self.expr1.evaluate(env)
        # Ritorna il risultato memorizzato
        return result
    
    def __str__(self):
        return f"prog4 ({self.expr1}, {self.expr2}, {self.expr3}, {self.expr4})"
    

class If(Expression):
    # If valuta una condizione e esegue una delle due espressioni a seconda del risultato della condizione

    arity = 3

    def __init__(self, args):
        self.if_no = args[0]   # L'espressione da eseguire se la condizione è falsa
        self.if_yes = args[1]  # L'espressione da eseguire se la condizione è vera
        self.cond = args[2]    # La condizione da valutare

    def evaluate(self, env):
        # Gestisce la condizione come espressione, nome di variabile o valore costante
        if isinstance(self.cond, Expression):
            condition_result = self.cond.evaluate(env)

        elif isinstance(self.cond, str):
            if self.cond in env:
                condition_result = env[self.cond]
            else:
                raise MissingVariableException(f"Valore mancante per la variabile '{self.cond}'")
        else:
            condition_result = self.cond  # Se è un valore costante

        # Valuta if-yes o if-no a seconda del risultato della condizione
        if condition_result:
            return self.if_yes.evaluate(env) if isinstance(self.if_yes, Expression) else self.if_yes
        else:
            return self.if_no.evaluate(env) if isinstance(self.if_no, Expression) else self.if_no

    def __str__(self):
        return f"if({self.if_no}, {self.if_yes}, {self.cond})"


    
class While(Expression):
    # While esegue un'espressione ripetutamente finché una condizione specificata è vera

    arity = 2

    def __init__(self, args):
        self.expr = args[0]  # L'espressione da eseguire nel ciclo
        self.cond = args[1]  # La condizione che determina l'esecuzione del ciclo
        
    def evaluate(self, env):
        while self.cond.evaluate(env):  # Continua finché la condizione è vera
            self.expr.evaluate(env)     # Esegui l'espressione all'interno del ciclo
        return None

    def __str__(self):
        return f"while({self.expr}, {self.cond})"

    

class For(Expression):
    # For esegue un'espressione per un numero specificato di volte, controllato da un indice

    arity = 4

    def __init__(self, args):
        self.expr = args[0]   # L'espressione da eseguire all'interno del ciclo
        self.end = args[1]    # Il valore finale del ciclo
        self.start = args[2]  # Il valore iniziale del ciclo
        self.i_var = args[3]  # La variabile di controllo dell'indice

    def evaluate(self, env):
        # Valuta start e end come espressioni
        start_val = self.start.evaluate(env) if isinstance(self.start, Expression) else self.start
        end_val = self.end.evaluate(env) if isinstance(self.end, Expression) else self.end
        i_var_name = str(self.i_var)

        for i in range(start_val, end_val):
            env[i_var_name] = i  # Assegna il valore dell'indice alla variabile di controllo
            self.expr.evaluate(env)  # Esegui l'espressione all'interno del ciclo
        return None

    def __str__(self):
        return f"for({self.expr}, from {self.start} to {self.end}, var {self.i_var})"



class DefSub(Expression):
# DefSub definisce una subroutine (funzione) e la associa a un nome nell'ambiente

    arity = 2

    def __init__(self, args):
        self.expr = args[0]
        self.function_name = args[1]

    def evaluate(self, env):
        # Associa l'espressione alla variabile senza valutarla
        env[str(self.function_name)] = self.expr
        return None

    def __str__(self):
        return f"defsub({self.expr}, {self.function_name})"


class Call(Expression):
# Call esegue una subroutine definita precedentemente nell'ambiente

    arity = 1

    def __init__(self, args):
        self.function_name = args[0]

    def evaluate(self, env):
        # Recupera la subroutine dal nome della funzione nell'ambiente
        if str(self.function_name) in env:
            function_expr = env[str(self.function_name)]
            return function_expr.evaluate(env)
        else:
            raise FunctionNotFoundException(f"La subroutine '{self.function_name}' non è definita")

    def __str__(self):
        return f"call({self.function_name})"


class Print(Expression):
# Print stampa il risultato di un'espressione nell'ambiente

    arity = 1

    def __init__(self, args):
        self.expr = args[0]

    def evaluate(self, env):
        if isinstance(self.expr, Expression):
            result = self.expr.evaluate(env)
        elif isinstance(self.expr, str):  # Gestisce i nomi delle variabili
            if self.expr in env:
                result = env[self.expr]
            else:
                raise MissingVariableException(f"Valore mancante per la variabile '{self.expr}'")
        else:
            result = self.expr  # Gestisce i valori costanti

        print(result)
        return result

    def __str__(self):
        return f"print({self.expr})"


class Nop(Expression):
# Nop rappresenta un'operazione che non esegue alcuna azione (No Operation)
    
    arity = 0

    def __init__(self):
        pass

    def evaluate(self, env):
        # Non fa nulla
        return None

    def __str__(self):
        return "nop"

    
class BinaryOp(Operation):
    # Classe base per operazioni binarie (due operandi)
    arity = 2

    def __init__(self, args):
        self.x = args[0]
        self.y = args[1]
        super().__init__([self.x, self.y])


class UnaryOp(Operation):
    # Classe base per operazioni unarie (un solo operando)
    arity = 1

    def __init__(self, args):
        self.x = args[0]
        super().__init__([self.x])


class Addition(BinaryOp):
    # Implementa l'addizione
    def op(self, x, y):
        return y + x
    
    def __str__(self):
        return f"(+ {self.args[0]} {self.args[1]})"


class Subtraction(BinaryOp):
    # Implementa la sottrazione
    def op(self, x, y):
        return y - x
    
    def __str__(self):
        return f"(- {self.args[0]} {self.args[1]})"


class Division(BinaryOp):
    # Implementa la divisione
    def op(self, x, y):
        if x == 0:
            raise DivisionByZeroException("La divisione per zero non è consentita")
        return y / x

    def __str__(self):
        return f"(/ {self.args[0]} {self.args[1]})"


class Multiplication(BinaryOp):
    # Implementa la moltiplicazione
    def op(self, x, y):
        return y * x
    
    def __str__(self):
        return f"(* {self.args[0]} {self.args[1]})"


class Power(BinaryOp):
    # Implementa l'elevazione a potenza
    def op(self, x, y):
        return y ** x
    
    def __str__(self):
        return f"(** {self.args[0]} {self.args[1]})"


class Modulus(BinaryOp):
    # Implementa l'operazione di modulo
    def op(self, x, y):
        return y % x
    
    def __str__(self):
        return f"(% {self.args[0]} {self.args[1]})"


class Reciprocal(UnaryOp):
    # Implementa il calcolo del reciproco di un numero
    def op(self, y):
        if y == 0:
            raise DivisionByZeroException("La divisione per zero non è consentita")
        return 1 / y
    
    def __str__(self):
        return f"(1/ {self.args[0]})"


class AbsoluteValue(UnaryOp):
    # Calcola il valore assoluto di un numero
    def op(self, y):
        return abs(y)

    def __str__(self):
        return f"abs({self.args[0]})"
    

class Major(BinaryOp):
    # Confronta due valori per determinare se il primo è maggiore del secondo
    def op(self, x, y):
        return y > x

    def __str__(self):
        return f"(> {self.args[0]} {self.args[1]})"


class Minor(BinaryOp):
    # Confronta due valori per determinare se il primo è minore del secondo
    def op(self, x, y):
        return y < x

    def __str__(self):
        return f"(< {self.args[0]} {self.args[1]})"


class MajorEq(BinaryOp):
    # Confronta due valori per determinare se il primo è maggiore o uguale al secondo
    def op(self, x, y):
        return y >= x

    def __str__(self):
        return f"(>= {self.args[0]} {self.args[1]})"


class MinorEq(BinaryOp):
    # Confronta due valori per determinare se il primo è minore o uguale al secondo
    def op(self, x, y):
        return y <= x

    def __str__(self):
        return f"(<= {self.args[0]} {self.args[1]})"


class Equal(BinaryOp):
    # Confronta due valori per determinare se sono uguali
    def op(self, x, y):
        return y == x

    def __str__(self):
        return f"(= {self.args[0]} {self.args[1]})"


class NotEqual(BinaryOp):
    # Confronta due valori per determinare se sono diversi
    def op(self, x, y):
        return y != x

    def __str__(self):
        return f"(!= {self.args[0]} {self.args[1]})"


# Dizionario delle operazioni supportate con le relative classi di operazione corrispondenti
d = {
    "+": Addition,
    "-": Subtraction,
    "/": Division,
    "*": Multiplication, 
    "**": Power,
    "%": Modulus, 
    "1/": Reciprocal, 
    "abs": AbsoluteValue,
    ">": Major,
    "<": Minor,
    ">=": MajorEq,
    "<=": MinorEq,
    "=": Equal,
    "!=": NotEqual,
    "alloc": Alloc,
    "valloc": Valloc,
    "setq": Setq,
    "setv":Setv,
    "prog2": Prog2,
    "prog3": Prog3,
    "prog4": Prog4,
    "if": If,
    "while": While,
    "for": For,
    "defsub": DefSub,
    "call": Call,
    "print": Print,
    "nop": Nop
    }

example = "nop x print prime if nop 0 0 != prime setq i x % 0 = if 1 x - 2 i for 0 0 = prime setq prime alloc prog4 100 2 x for"
e = Expression.from_program(example, d)
print(e)
res = e.evaluate({})
print(res)

"""
Esempi di codice project_python.pdf + teams:
2 x + x alloc prog2
x 1 + x setq x 10 > while x alloc prog2
v print i i * i v setv prog2 10 0 i for 10 v valloc prog2
x print f call x alloc x 4 + x setq f defsub prog4
nop i print i x % 0 = if 1000 2 i for 783 x setq x alloc prog3
nop x print prime if nop 0 0 != prime setq i x % 0 = if 1 x - 2 i for 0 0 = prime setq prime alloc prog4 100 2 x for
v print i j * 1 i - 10 * 1 j - + v setv 11 1 j for 11 1 i for 100 v valloc prog3
x print 1 3 x * + x setq 2 x / x setq 2 x % 0 = if prog2 1 x != while 50 x setq x alloc prog3

Espressione base instruction.pdf - Esercitazione n°11:
2 3 + x * 6 5 - / abs 2 ** y 1/ + 1/
"x":3,"y":7
Output atteso:
(1/ (+ (1/ y) (** 2 (abs (/ (- 5 6) (* x (+ 3 2)))))))    
0.84022932953024
"""