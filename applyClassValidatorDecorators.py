#! /usr/bin/python3
import sys

def determineDecorators(property, sqlite,  explicit):
    colon_index = property.find(":")
    typeUnion = property[colon_index:]
    decorators = []
    if explicit:
        decorators.append("@ApiProperty()")

    if "null" in typeUnion:
        decorators.append("@IsNullable()")
    if "string" in typeUnion:
        decorators.append("@IsString()")
    if "boolean" in typeUnion:
        if sqlite:
            decorators.append("@TransformBoolean()")
        else:
            decorators.append("@IsBoolean()")
    if "number" in typeUnion:
        decorators.append("@IsNumber()")
    if "Date" in typeUnion:
        decorators.append("@IsDateString()")

    return decorators

def getDefinitionStart(fileContents, className):
    start_index = fileContents.find(f" {className} " )
    if start_index < 0:
        print("Error check the class name and try again")
        exit(-1)
    definitionStart = fileContents.find("{", start_index) + 1
    return definitionStart

def getDefinitionEnd(file_contents, definitionStart):
    return file_contents.find("}\n", definitionStart)
def parseClassDefinition(fileContents, className):
    definitionStart = getDefinitionStart(fileContents, className)
    definitionEnd = getDefinitionEnd(fileContents, definitionStart)
    definitions = fileContents[definitionStart:definitionEnd]

    return definitions.split("\n")
  
def read_contents_of_file(file_path):
    file_contents = ''
    with open(file_path) as file:
        file_contents = file.read()
    return file_contents

def write_to_file(file_path, contents):
    with open(file_path, "w") as file:
        file.write(contents)

def main():
    file_contents = read_contents_of_file(sys.argv[1])
    propertyDefinitions = parseClassDefinition(file_contents, sys.argv[2])
    definitionStart = getDefinitionStart(file_contents, sys.argv[2])
    definitionEnd = getDefinitionEnd(file_contents, definitionStart)
    
    explicit = False
    if len(sys.argv) == 5 and sys.argv[4] == 'explicit':
        explicit = True

    sqlite = False
    if len(sys.argv) >= 4 and sys.argv[3] == 'sqlite':
        sqlite = True
    
    newFileContents = file_contents[:definitionStart]

    for property in propertyDefinitions:
        decorators ="\n\n" + "\n".join(determineDecorators(property, sqlite, explicit))
        newFileContents += decorators + "\n" + property


    newFileContents += file_contents[definitionEnd:]
    write_to_file(sys.argv[1], newFileContents)

main()
