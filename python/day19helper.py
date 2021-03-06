#!python3


import re


TEST_INPUT_1 = '''0: 1 2
1: "a"
2: 1 3 | 3 1
3: "b"
'''

TEST_INPUT_2 = '''0: 4 1 5
1: 2 3 | 3 2
2: 4 4 | 5 5
3: 4 5 | 5 4
4: "a"
5: "b"
'''

TEST_RE = '''ababbb
bababa
abbbab
aaabbb
aaaabbb
'''


CHAR = 'CHAR'
NUM = 'NUM'
OR = 'OR'
OPEN_PAREN = 'OPEN_PAREN'
CLOSE_PAREN = 'CLOSE_PAREN'
ONE_OR_MORE = 'ONE_OR_MORE'
EOF = 'EOF'


class Token(object):
    def __init__(self, token_type, value):
        self.type = token_type
        self.value = value


    @classmethod
    def one_or_more(cls):
        return cls(ONE_OR_MORE, '+')


    @classmethod
    def eof(cls):
        return cls(EOF, None)


    @property
    def char(self):
        self.value


    def __repr__(self):
        return f'Token({self.type}, {self.value})'


class Lexer(object):
    def __init__(self, text):
        if '|' in text:
            text = '( ' + text + ' )'
        self.text = text
        self.position = 0


    def get_next_token(self):
        if self.is_at_end:
            return Token.eof()
        while self.text[self.position] == ' ':
            self.position += 1
        ch = self.text[self.position]
        if ch == '|':
            self.position += 1
            return Token(OR, '|')
        elif ch == '(':
            self.position += 1
            return Token(OPEN_PAREN, '(')
        elif ch == ')':
            self.position += 1
            return Token(CLOSE_PAREN, ')')
        elif ch.isdigit():
            result = ch
            self.position += 1
            while not self.is_at_end and self.text[self.position].isdigit():
                result += self.text[self.position]
                self.position += 1
            return Token(NUM, int(result))
        elif ch == '"':
            self.position += 1
            token = Token(CHAR, self.text[self.position])
            self.position += 2
            return token
        else:
            raise Exception(f'Invalid token: {ch}')


    def get_all_tokens(self):
        all_tokens = []
        while True:
            token = self.get_next_token()
            if token.type == EOF:
                return all_tokens
            all_tokens.append(token)
        return all_tokens


    @property
    def is_at_end(self):
        return self.position >= len(self.text)


class Parser(object):
    def __init__(self, rules):
        self.rules = rules


    def parse(self, n):
        all_tokens = [t for t in self.rules[n]]
        more_parsing = True
        while more_parsing:
            more_parsing = False
            new_tokens = []
            for token in all_tokens:
                if token.type == NUM:
                    more_parsing = True
                    other_tokens = self.rules[token.value]
                    new_tokens.extend(other_tokens)
                else:
                    new_tokens.append(token)
            all_tokens = new_tokens
        return all_tokens


def make_rule(text, part2=False):
    number, rule = text.split(': ')
    number = int(number)
    part2_i = 7
    if part2 and number == 8:
        rule = ' | '.join('42 '*i for i in range(1, part2_i))
    if part2 and number == 11:
        rule = ' | '.join('42 '*i + '31 '*i for i in range(1, part2_i))
    l = Lexer(rule)
    tokens = l.get_all_tokens()
    return number, tokens


def make_rules(text, part2=False):
    rules = {}
    for line in text.strip().split('\n'):
        n, r = make_rule(line, part2=part2)
        rules[n] = r
    return rules


def make_partial_re(text, n, part2=False):
    rules = make_rules(text, part2=part2)
    p = Parser(rules)
    r = p.parse(n)
    return ''.join(a.value for a in r)


def make_re(text, n, part2=False):
    '''n is rule number.'''
    rules = make_rules(text, part2=part2)
    p = Parser(rules)
    r = p.parse(n)

    x = ''.join(a.value for a in r)
    prog = re.compile('^' + x + '$')
    return prog


def test1():
    prog = make_re(TEST_INPUT_2, 0)
    for test in TEST_RE.strip().split('\n'):
        m = prog.match(test)
        print(test)
        print(m)


def main():
    test1()


if __name__ == "__main__":
    main()
