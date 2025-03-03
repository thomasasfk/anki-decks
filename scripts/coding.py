from base import AnkiDeck, DeckMetadata
import genanki
import os
import tempfile
import shutil


class JavaFundamentalsDeck(AnkiDeck):
    def create_model(self) -> genanki.Model:
        return genanki.Model(
            self._model_id,
            'Java Fundamentals Card',
            fields=[
                {'name': 'Question'},
                {'name': 'Answer'},
                {'name': 'QuestionNumber'},
                {'name': 'Tags'}
            ],
            templates=[{
                'name': 'Java Practice',
                'qfmt': '''
                <div class="card">
                    <div class="question-number">Question {{QuestionNumber}}</div>
                    <div class="question">{{Question}}</div>
                    <div class="answer-box">
                        <div class="code-hint">Write your answer here:</div>
                        <div class="code-textarea" contenteditable="true" id="userAnswer"></div>
                    </div>
                    <div class="tags">{{Tags}}</div>
                </div>

                <script>
                // Immediately executing script to set up persistence
                (function() {
                    try {
                        // Get the current question number and generate a unique key
                        var questionNumber = "{{QuestionNumber}}";
                        var storageKey = "java_answer_" + questionNumber;
                        var sessionKey = "java_current_session";
                        var userAnswer = document.getElementById("userAnswer");

                        // Create or update unique session ID whenever a question card is shown
                        // This helps differentiate between review sessions
                        if (!localStorage.getItem(sessionKey)) {
                            localStorage.setItem(sessionKey, Date.now().toString());
                        }

                        // Don't load previous answer on front side of card - always start fresh
                        // Just set up the save functionality

                        // Save answer whenever content changes
                        userAnswer.addEventListener("input", function() {
                            try {
                                localStorage.setItem(storageKey, this.innerHTML);
                            } catch (e) {
                                console.error("Failed to save: " + e.message);
                            }
                        });

                        // Also handle blur (when user clicks away) for extra reliability
                        userAnswer.addEventListener("blur", function() {
                            try {
                                localStorage.setItem(storageKey, this.innerHTML);
                            } catch (e) {
                                console.error("Failed to save on blur: " + e.message);
                            }
                        });
                    } catch (e) {
                        console.error("Error in setup: " + e.message);
                    }
                })();
                </script>
                ''',
                'afmt': '''
                <div class="card">
                    <div class="question-number">Question {{QuestionNumber}}</div>
                    <div class="question">{{Question}}</div>
                    <div class="answer-box">
                        <div class="code-hint">Your answer:</div>
                        <div class="code-textarea user-answer" id="userAnswer"></div>
                    </div>
                    <div class="solution">
                        <div class="solution-title">Solution:</div>
                        <div class="solution-content">{{Answer}}</div>
                    </div>
                    <div class="tags">{{Tags}}</div>
                </div>

                <script>
                // Immediately executing script to load the saved answer
                (function() {
                    try {
                        // Get the current question number
                        var questionNumber = "{{QuestionNumber}}";
                        var storageKey = "java_answer_" + questionNumber;
                        var userAnswer = document.getElementById("userAnswer");

                        // Load previous answer if available
                        var savedAnswer = localStorage.getItem(storageKey);
                        if (savedAnswer && savedAnswer.trim() !== "") {
                            userAnswer.innerHTML = savedAnswer;
                        } else {
                            userAnswer.innerHTML = "// No answer provided";
                        }

                        // Ensure it's not editable in the answer view
                        userAnswer.setAttribute("contenteditable", "false");

                        console.log("Loaded saved answer for question " + questionNumber);
                    } catch (e) {
                        console.error("Error loading saved answer: " + e.message);
                        userAnswer.innerHTML = "// Error loading your answer: " + e.message;
                    }
                })();
                </script>
                '''
            }],
            css=self.get_custom_css()
        )

    def get_custom_css(self) -> str:
        return '''
        .card {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            background-color: #1a1a1a;
            color: #ffffff;
            padding: 20px;
            max-width: 800px;
            margin: 0 auto;
            font-size: 16px;
            line-height: 1.5;
        }
        .question-number {
            font-size: 1.2em;
            font-weight: bold;
            color: #4CAF50;
            margin-bottom: 10px;
        }
        .question {
            font-size: 1.1em;
            margin-bottom: 20px;
            white-space: pre-wrap;
        }
        .answer-box {
            margin-bottom: 20px;
        }
        .code-hint {
            color: #999;
            font-style: italic;
            margin-bottom: 5px;
        }
        .code-textarea {
            background-color: #2d2d2d;
            border: 1px solid #555;
            border-radius: 5px;
            padding: 10px;
            font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
            min-height: 150px;
            white-space: pre;
            color: #f8f8f8;
        }
        .user-answer {
            border: 1px solid #4CAF50;
            margin-bottom: 20px;
        }
        .solution {
            margin-top: 20px;
            border-top: 1px solid #555;
            padding-top: 15px;
        }
        .solution-title {
            font-weight: bold;
            color: #4CAF50;
            margin-bottom: 10px;
        }
        .solution-content {
            background-color: #2d2d2d;
            padding: 15px;
            border-radius: 5px;
            white-space: pre;
            font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
        }
        .tags {
            margin-top: 15px;
            font-style: italic;
            color: #888;
            font-size: 0.9em;
        }
        img {
            max-width: 100%;
            height: auto;
            border-radius: 8px;
            margin: 10px 0;
        }
        .nightMode {
            background-color: #1a1a1a;
            color: #ffffff;
        }
        '''

    def generate_cards(self) -> list[genanki.Note]:
        cards = []

        # Card 1: Create a Simple Class with an Object
        cards.append(
            genanki.Note(
                model=self.create_model(),
                fields=[
                    "Define a class called Person with the following:\n• Fields: name (String) and age (int)\n• A method printDetails() that prints the name and age.\n• In the main method, create an object of Person, set values, and call printDetails().",

                    """public class Person {
    String name;
    int age;

    void printDetails() {
        System.out.println("Name: " + name);
        System.out.println("Age: " + age);
    }

    public static void main(String[] args) {
        Person person = new Person();
        person.name = "Alice";
        person.age = 25;
        person.printDetails();
    }
}""",
                    "1",
                    "class, object, basic"
                ]
            )
        )

        # Card 2: Demonstrate toString() Method
        cards.append(
            genanki.Note(
                model=self.create_model(),
                fields=[
                    "Modify the Person class to add the toString() method.\n• The method should return \"Person[name=Alice, age=25]\"\n• In the main method, print the object directly.",

                    """public class Person {
    String name;
    int age;

    @Override
    public String toString() {
        return "Person[name=" + name + ", age=" + age + "]";
    }

    public static void main(String[] args) {
        Person person = new Person();
        person.name = "Alice";
        person.age = 25;
        System.out.println(person);
    }
}""",
                    "2",
                    "toString, override"
                ]
            )
        )

        # Card 3: Demonstrate Constructors
        cards.append(
            genanki.Note(
                model=self.create_model(),
                fields=[
                    "Modify the Person class to include:\n• A constructor that initializes name and age.\n• Create an object using the constructor and print the details.",

                    """public class Person {
    String name;
    int age;

    Person(String name, int age) {
        this.name = name;
        this.age = age;
    }

    void printDetails() {
        System.out.println("Name: " + name);
        System.out.println("Age: " + age);
    }

    public static void main(String[] args) {
        Person person = new Person("John", 30);
        person.printDetails();
    }
}""",
                    "3",
                    "constructor"
                ]
            )
        )

        # Card 4: Method with Parameters and Return Type
        cards.append(
            genanki.Note(
                model=self.create_model(),
                fields=[
                    "Write a class named Calculator. In the class write a method sum(int a, int b) that takes two integers as parameters and returns their sum.",

                    """public class Calculator {
    int sum(int a, int b) {
        return a + b;
    }

    public static void main(String[] args) {
        Calculator calc = new Calculator();
        int result = calc.sum(5, 3);
        System.out.println("Sum: " + result);
    }
}""",
                    "4",
                    "methods, parameters, return"
                ]
            )
        )

        # Card 5: Read and Print an Integer
        cards.append(
            genanki.Note(
                model=self.create_model(),
                fields=[
                    "Write a Java program that:\n• Uses Scanner to read an integer from the user.\n• Prints the entered number using System.out.println().",

                    """import java.util.Scanner;

public class ReadInteger {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        System.out.print("Enter a number: ");
        int number = scanner.nextInt();

        System.out.println("You entered: " + number);

        scanner.close();
    }
}""",
                    "5",
                    "scanner, input, integer"
                ]
            )
        )

        # Card 6: Read and Print a Floating-Point Number
        cards.append(
            genanki.Note(
                model=self.create_model(),
                fields=[
                    "Write a program that:\n• Reads a floating-point number from the user.\n• Prints it using System.out.printf() with two decimal places.",

                    """import java.util.Scanner;

public class ReadFloat {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        System.out.print("Enter a number: ");
        double number = scanner.nextDouble();

        System.out.printf("You entered: %.2f%n", number);

        scanner.close();
    }
}""",
                    "6",
                    "scanner, input, float, printf"
                ]
            )
        )

        # Card 7: Read and Print a String
        cards.append(
            genanki.Note(
                model=self.create_model(),
                fields=[
                    "Write a Java program that:\n• Reads a string using Scanner.nextLine().\n• Prints the entered string using System.out.println().",

                    """import java.util.Scanner;

public class ReadString {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        System.out.print("Enter your name: ");
        String name = scanner.nextLine();

        System.out.println("Hello, " + name + "!");

        scanner.close();
    }
}""",
                    "7",
                    "scanner, input, string, nextLine"
                ]
            )
        )

        # Card 8: Add Two Integers
        cards.append(
            genanki.Note(
                model=self.create_model(),
                fields=[
                    "Write a Java program that:\n• Reads two integers from the user.\n• Calculates their sum and prints it.",

                    """import java.util.Scanner;

public class AddIntegers {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        System.out.print("Enter first number: ");
        int num1 = scanner.nextInt();

        System.out.print("Enter second number: ");
        int num2 = scanner.nextInt();

        int sum = num1 + num2;
        System.out.println("Sum: " + sum);

        scanner.close();
    }
}""",
                    "8",
                    "addition, scanner, input"
                ]
            )
        )

        # Card 9: Multiply Two Floating-Point Numbers
        cards.append(
            genanki.Note(
                model=self.create_model(),
                fields=[
                    "Write a Java program that:\n• Reads two floating-point numbers from the user.\n• Prints their product using printf() with two decimal places.",

                    """import java.util.Scanner;

public class MultiplyFloats {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        System.out.print("Enter first number: ");
        double num1 = scanner.nextDouble();

        System.out.print("Enter second number: ");
        double num2 = scanner.nextDouble();

        double product = num1 * num2;
        System.out.printf("Product: %.2f%n", product);

        scanner.close();
    }
}""",
                    "9",
                    "multiplication, scanner, float, printf"
                ]
            )
        )

        # Card 10: Calculate Area of a Circle
        cards.append(
            genanki.Note(
                model=self.create_model(),
                fields=[
                    "Write a Java program that:\n• Reads the radius of a circle from the user.\n• Calculates and prints the area using π * r², formatted to two decimal places.",

                    """import java.util.Scanner;

public class CircleArea {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        System.out.print("Enter radius: ");
        double radius = scanner.nextDouble();

        double area = Math.PI * radius * radius;
        System.out.printf("Area of circle: %.2f%n", area);

        scanner.close();
    }
}""",
                    "10",
                    "circle, area, Math.PI, printf"
                ]
            )
        )

        # Card 11: Read Name and Age, Then Print a Sentence
        cards.append(
            genanki.Note(
                model=self.create_model(),
                fields=[
                    "Write a Java program that:\n• Reads a name and an age from the user.\n• Prints a sentence using printf().",

                    """import java.util.Scanner;

public class NameAge {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        System.out.print("Enter your name: ");
        String name = scanner.nextLine();

        System.out.print("Enter your age: ");
        int age = scanner.nextInt();

        System.out.printf("%s is %d years old.%n", name, age);

        scanner.close();
    }
}""",
                    "11",
                    "printf, scanner, multiple inputs"
                ]
            )
        )

        # Card 12: Read Three Numbers and Print Their Average
        cards.append(
            genanki.Note(
                model=self.create_model(),
                fields=[
                    "Write a Java program that:\n• Reads three numbers from the user.\n• Computes and prints their average to two decimal places.",

                    """import java.util.Scanner;

public class Average {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        System.out.print("Enter three numbers: ");
        double num1 = scanner.nextDouble();
        double num2 = scanner.nextDouble();
        double num3 = scanner.nextDouble();

        double average = (num1 + num2 + num3) / 3;
        System.out.printf("Average: %.2f%n", average);

        scanner.close();
    }
}""",
                    "12",
                    "average, scanner, multiple inputs, printf"
                ]
            )
        )

        # Card 13: Read a Character and Print Its ASCII Value
        cards.append(
            genanki.Note(
                model=self.create_model(),
                fields=[
                    "Write a Java program that:\n• Reads a character from the user.\n• Prints its ASCII value.",

                    """import java.util.Scanner;

public class AsciiValue {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        System.out.print("Enter a character: ");
        char ch = scanner.next().charAt(0);

        int ascii = (int) ch;
        System.out.println("ASCII value of '" + ch + "': " + ascii);

        scanner.close();
    }
}""",
                    "13",
                    "ascii, char, type casting"
                ]
            )
        )

        # Card 14: Create a Simple Class with Fields and a Method
        cards.append(
            genanki.Note(
                model=self.create_model(),
                fields=[
                    "Create a class Person with the following:\n• Fields: name (String) and age (int)\n• Method printDetails() that prints the name and age\n• Create a Person object in the main method and call printDetails()",

                    """public class Person {
    String name;
    int age;

    void printDetails() {
        System.out.println("Name: " + name);
        System.out.println("Age: " + age);
    }

    public static void main(String[] args) {
        Person person = new Person();
        person.name = "Alice";
        person.age = 25;
        person.printDetails();
    }
}""",
                    "14",
                    "class, fields, methods, objects"
                ]
            )
        )

        # Card 15: Create a Class with a Constructor
        cards.append(
            genanki.Note(
                model=self.create_model(),
                fields=[
                    "Modify the Person class to include:\n• A constructor that initializes name and age\n• In main(), create a Person object using the constructor and print the details",

                    """public class Person {
    String name;
    int age;

    Person(String name, int age) {
        this.name = name;
        this.age = age;
    }

    void printDetails() {
        System.out.println("Person created: " + name + ", Age: " + age);
    }

    public static void main(String[] args) {
        Person person = new Person("Alice", 25);
        person.printDetails();
    }
}""",
                    "15",
                    "constructor, this keyword"
                ]
            )
        )

        # Card 16: Using Getters and Setters
        cards.append(
            genanki.Note(
                model=self.create_model(),
                fields=[
                    "Create a class Car with:\n• Private fields: brand (String) and year (int)\n• Public getter and setter methods for both fields\n• In main(), create a Car object, set values, and print them",

                    """public class Car {
    private String brand;
    private int year;

    public String getBrand() {
        return brand;
    }

    public void setBrand(String brand) {
        this.brand = brand;
    }

    public int getYear() {
        return year;
    }

    public void setYear(int year) {
        this.year = year;
    }

    public static void main(String[] args) {
        Car car = new Car();
        car.setBrand("Toyota");
        car.setYear(2020);

        System.out.println("Car Brand: " + car.getBrand());
        System.out.println("Manufactured Year: " + car.getYear());
    }
}""",
                    "16",
                    "getters, setters, encapsulation, private"
                ]
            )
        )

        # Card 17: Method Returning a Value
        cards.append(
            genanki.Note(
                model=self.create_model(),
                fields=[
                    "Create a class Rectangle with:\n• Fields length and width\n• Method calculateArea(int length, int width) that returns the area\n• In main(), create a Rectangle object and print its area",

                    """public class Rectangle {
    int length;
    int width;

    int calculateArea(int length, int width) {
        return length * width;
    }

    public static void main(String[] args) {
        Rectangle rect = new Rectangle();
        int area = rect.calculateArea(10, 5);
        System.out.println("Area: " + area);
    }
}""",
                    "17",
                    "methods, return value, parameters"
                ]
            )
        )

        # Card 18: Overloading Constructors
        cards.append(
            genanki.Note(
                model=self.create_model(),
                fields=[
                    "Modify the Rectangle class to include:\n• A constructor with parameters (length, width)\n• A default constructor that sets default values\n• Create two Rectangle objects using both constructors and print their areas",

                    """public class Rectangle {
    int length;
    int width;

    Rectangle() {
        this.length = 5;
        this.width = 4;
    }

    Rectangle(int length, int width) {
        this.length = length;
        this.width = width;
    }

    int calculateArea() {
        return length * width;
    }

    public static void main(String[] args) {
        Rectangle rect1 = new Rectangle(10, 5);
        Rectangle rect2 = new Rectangle();

        System.out.println("Area of rectangle 1: " + rect1.calculateArea());
        System.out.println("Area of rectangle 2: " + rect2.calculateArea());
    }
}""",
                    "18",
                    "constructor overloading, default constructor"
                ]
            )
        )

        # Card 19: toString() Method Override
        cards.append(
            genanki.Note(
                model=self.create_model(),
                fields=[
                    "Create a class Book with:\n• Fields: title and author\n• Override the toString() method to return book details\n• Create a Book object in main() and print it",

                    """public class Book {
    String title;
    String author;

    Book(String title, String author) {
        this.title = title;
        this.author = author;
    }

    @Override
    public String toString() {
        return "Book[Title=" + title + ", Author=" + author + "]";
    }

    public static void main(String[] args) {
        Book book = new Book("Java Basics", "John Doe");
        System.out.println(book);
    }
}""",
                    "19",
                    "toString, override, object methods"
                ]
            )
        )

        # Card 20: Implement a Bank Account Class
        cards.append(
            genanki.Note(
                model=self.create_model(),
                fields=[
                    "Create a class BankAccount with:\n• Fields: accountNumber, balance\n• Methods: deposit(double amount), withdraw(double amount), printBalance()\n• In main(), create a BankAccount object and test all methods",

                    """public class BankAccount {
    String accountNumber;
    double balance;

    BankAccount(String accountNumber) {
        this.accountNumber = accountNumber;
        this.balance = 0;
    }

    void deposit(double amount) {
        System.out.println("Depositing $" + amount + "...");
        balance += amount;
        printBalance();
    }

    void withdraw(double amount) {
        if (amount <= balance) {
            System.out.println("Withdrawing $" + amount + "...");
            balance -= amount;
        } else {
            System.out.println("Insufficient funds!");
        }
        printBalance();
    }

    void printBalance() {
        System.out.println("New Balance: $" + balance);
    }

    public static void main(String[] args) {
        BankAccount account = new BankAccount("123456");
        account.deposit(500);
        account.withdraw(200);
    }
}""",
                    "20",
                    "methods, object state, banking application"
                ]
            )
        )

        return cards


if __name__ == "__main__":
    # Create temporary media directory for any media files
    media_dir = tempfile.mkdtemp()

    try:
        # Create and save the deck
        deck = JavaFundamentalsDeck(
            DeckMetadata(
                title="Java Programming Fundamentals",
                tags=["java", "programming", "beginners", "practice"],
                description="A comprehensive deck covering Java programming fundamentals with 20 practice questions. Each card provides a programming problem with a solution to help you learn and practice Java syntax and concepts.",
                version="1.0"
            )
        )

        deck.save_deck("java_fundamentals_deck.apkg")

        print("Anki deck 'java_fundamentals_deck.apkg' created successfully!")

    finally:
        # Clean up any temporary media files
        if os.path.exists(media_dir):
            shutil.rmtree(media_dir)