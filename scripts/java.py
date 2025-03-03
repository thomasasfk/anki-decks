from base import AnkiDeck, DeckMetadata
import genanki


class JavaFundamentalsDeck(AnkiDeck):
    def create_model(self) -> genanki.Model:
        return genanki.Model(
            self._model_id,
            'Java Fundamentals QA',
            fields=[
                {'name': 'Question'},
                {'name': 'Answer'}
            ],
            templates=[{
                'name': 'Java Fundamentals Card',
                'qfmt': '<div class="question">{{Question}}</div>',
                'afmt': '{{FrontSide}}<hr><div class="answer">{{Answer}}</div>'
            }],
            css=self.get_default_css()
        )

    def generate_cards(self) -> list[genanki.Note]:
        # Define questions and answers
        qa_pairs = [
            # 1-10
            ("What is a variable in Java, and why is it important?",
             "A variable is a named storage location in memory that holds a value of a specific data type. It's important because it allows programs to store, retrieve, and manipulate data during execution."),

            ("How does a symbol table help a compiler during program execution?",
             "A symbol table stores information about identifiers (variables, methods, classes) including their names, types, scopes, and memory locations. It helps the compiler verify proper usage, resolve references, perform type checking, and generate appropriate code."),

            ("What is the difference between a local variable and an instance variable?",
             "Local variables are declared within methods and exist only while the method executes. Instance variables (fields) are declared in a class but outside any method and exist for the lifetime of the object instance."),

            ("What is the key difference between a primitive data type and a reference data type?",
             "Primitive data types store actual values directly in memory, while reference data types store memory addresses (references) that point to objects stored on the heap."),

            ("Name all eight primitive data types in Java.",
             "byte, short, int, long, float, double, char, boolean"),

            ("Explain the purpose of the null value in reference data types.",
             "null represents the absence of a value or reference - it indicates that a reference variable doesn't point to any object. It's used to explicitly show that a reference has no valid object associated with it."),

            ("What is the size (in bytes) of an int in Java?",
             "4 bytes (32 bits)"),

            ("What is the size (in bytes) of a reference variable in Java?",
             "Typically 4 bytes (32-bit JVM) or 8 bytes (64-bit JVM), depending on the JVM architecture."),

            ("Which Java primitive data type has the largest memory size?",
             "double (8 bytes/64 bits)"),

            ("How many bits are in a short in Java?",
             "16 bits (2 bytes)"),

            # 11-20
            ("What is the role of a Java compiler (javac) in program execution?",
             "The Java compiler translates human-readable Java source code (.java files) into bytecode (.class files) that can be executed by the Java Virtual Machine (JVM)."),

            ("How is the Java Runtime Environment (JRE) different from the Java Development Kit (JDK)?",
             "JRE is the runtime environment needed to run Java applications (includes JVM and class libraries). JDK is a superset of JRE that also includes development tools like the compiler (javac), debugger, and documentation tools needed to create Java applications."),

            (
            "For a given class named Person, what is the name of the file that stores its source code and what is the name of the file that stores its bytecode?",
            "Source code: Person.java\nBytecode: Person.class"),

            ("What is bytecode, and why is it important in Java?",
             "Bytecode is an intermediate, platform-independent code format that Java source code is compiled into. It's important because it enables Java's 'write once, run anywhere' capability - bytecode can be executed on any device with a JVM, regardless of the underlying hardware or operating system."),

            ("What does the Java Virtual Machine (JVM) do?",
             "The JVM loads, verifies, and executes Java bytecode. It handles memory management, garbage collection, security, and translates bytecode into machine-specific instructions, providing platform independence for Java applications."),

            ("Why is Java called a platform-independent language?",
             "Java is platform-independent because its compiled bytecode can run on any system with a compatible JVM, regardless of the underlying hardware architecture or operating system."),

            ("What is a class in Java, and what is its purpose?",
             "A class is a blueprint or template that defines the properties (fields) and behaviors (methods) that objects of that type will have. It serves as a framework for creating objects with shared characteristics and functionalities."),

            ("How does an object differ from a class?",
             "A class is a blueprint or template that defines properties and behaviors, while an object is an instance of a class - a concrete entity created from that blueprint with its own state (field values) and behavior (methods)."),

            ("How do you create an instance of a class in Java?",
             "You create an instance using the 'new' keyword followed by a constructor call: ClassName variableName = new ClassName();"),

            ("What is the purpose of the new keyword in Java?",
             "The 'new' keyword allocates memory on the heap for a new object instance, calls the constructor to initialize the object, and returns a reference to the newly created object."),

            # 21-30
            ("What is a field (instance variable) in a Java class?",
             "A field or instance variable is a variable declared within a class but outside any method. It stores data specific to each object instance of the class and represents the object's state or properties."),

            ("What is a method, and how does it differ from a field?",
             "A method is a block of code that performs a specific action or operation when called. While fields store data (state), methods define behavior - they operate on data and implement functionality."),

            ("What are parameters in a method? Give an example.",
             "Parameters are variables declared in a method signature that receive values passed to the method when it's called. Example: public void setAge(int age) { this.age = age; } - 'int age' is the parameter."),

            ("What is a return data type, and why is it necessary in Java methods?",
             "A return data type specifies what type of value a method will return after execution. It's necessary because Java is statically typed - the compiler needs to know what type of data to expect from a method call to ensure type safety and proper variable assignment."),

            ("What is the meaning of void in Java method declarations?",
             "void indicates that a method doesn't return any value. It performs actions but doesn't produce a result that needs to be assigned or used in expressions."),

            ("What is the purpose of a constructor in Java?",
             "A constructor initializes a new object when it's created. It sets initial values for object fields, allocates resources, and performs any setup operations needed before the object can be used."),

            ("How does a constructor differ from a regular method?",
             "Constructors have the same name as the class, have no return type (not even void), are automatically called when an object is created with 'new', and are specifically designed for initialization."),

            ("What is a default constructor, and when is it provided automatically?",
             "A default constructor is a no-argument constructor that initializes fields to their default values. Java automatically provides one only if a class has no explicit constructors defined."),

            ("Explain the purpose of the toString() method in Java.",
             "The toString() method returns a string representation of an object. It's used for debugging, logging, and displaying object information. By default, it returns the class name and hash code, but classes typically override it to provide meaningful string representations."),

            ("What is an overloaded method or constructor?",
             "An overloaded method or constructor has the same name but different parameter lists (different number or types of parameters). This allows multiple versions of the same method/constructor to handle different input types or amounts of data.")
        ]

        # Create notes from QA pairs
        notes = []
        for question, answer in qa_pairs:
            note = genanki.Note(
                model=self.create_model(),
                fields=[question, answer]
            )
            notes.append(note)

        return notes


if __name__ == "__main__":
    deck = JavaFundamentalsDeck(
        DeckMetadata(
            title="Java Fundamentals",
            tags=["java", "programming", "cs", "fundamentals"],
            description="A comprehensive deck covering Java fundamentals including variables, data types, classes, objects, methods, and more.",
            version="1.0",
        )
    )
    deck.save_deck("java_fundamentals.apkg")