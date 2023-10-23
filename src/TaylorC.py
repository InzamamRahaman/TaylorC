import grammar
import transpiler
from arpeggio import visit_parse_tree
from arpeggio import ParserPython
import argparse
from subprocess import call

if __name__ == '__main__':
    argparser = argparse.ArgumentParser()
    argparser.add_argument('filename')
    args = argparser.parse_args()
    with open(args.filename, 'r') as fp:
        file_contents = fp.read()

    program_parser = ParserPython(grammar.program)
    parse_tree = program_parser.parse(file_contents.strip())
    result = visit_parse_tree(parse_tree, transpiler.TaylorCTranspilerVisitor())[0]
    with open('temp.py', 'w') as fp:
        fp.write(result)
    call(["python", "temp.py"])


