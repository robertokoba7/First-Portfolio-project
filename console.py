#!/usr/bin/python3
"""Defines the Jumia clone console."""
import ast
import cmd
import re
from shlex import split
from models import storage
from models.base_model import BaseModel
from models.product import catalog
from models.shopping import cart
from models.user import login
from models.payment import payment
from models.support import support
from models.order import order


class JUMIACLONEcommand(cmd.Cmd):
    """This console contains the entry point of the command interpreter:

    Args:
        cmd ([commandline]): [it receives the command]

    Returns:
        [True, False]: [depends on the outcome]
    """
    prompt = '(jumiaclone)'

    def __init__(self, *args, **kwargs):
        self.factories = {
            "Basemodel": Basemodel,
            "catalog": productCatalog,
            "cart": ShoppingCart,
            "login": userlogin,
            "payment": paymentgateway,
            "support": customersupport,
            "order": ordermanagent
        }
        super().__init__(*args, **kwargs)

    def do_create(self, line):
        """ create an instance and save to json file"""
        args = args = line.split()
        if not args:
            print("**not found**")
            return
        class_name = args[0]
        if class_name not in self.factories:
            print("**invalid class name**")
            return
        obj = self.factories[class_name]()
        print(obj.id)
        obj.save()

    def create_help(self):
        """Documantation for create"""
        print("Handles the ctr+D signals to avoid errors")

    def do_quit(self, line):
        """exit command"""
        return True

    def help_quit(self):
        """quit docummentation"""
        print("Quit command to exit the program")

    def do_EOF(self, line):
        """ctr+D signal handler. The cmd.Cmd class expects the method to accept a single argument representing the user input line"""
        print("Handle the ctr+D to avoid error")

    def help_EOF(self):
        """EOF documentation"""
        print("Handle the ctr+D signal to avoid errors")

    def do_show(self, line):
        """Show an instance based on the class name and id"""
        args = []
        args = line.split()
        objects = storage.all()
        classes = ["Basemodel", "catalog", "cart", "login",
                   "payment", "support", "order"]
        if len(args) == 0:
            print("**class name not found**")
        elif args[0] not in classes:
            print("**class name missing**")
        elif len(args) <= 1:
            print("**instance id missing**")
        elif objects.get(args[0] + "." + args[1]) is not None:
            print(objects.get(args[0] + "." + args[1]))
        else:
            print("**no instance found**")

    def help_show(self):
        """show documentation"""
        print("Handle the ctr+D signal to avoid errors")

    def do_destroy(self, line):
        """Delete an instance based on class and id"""
        args = line.split()
        objects = storage.all()
        classes = ["Basemodel", "catalog", "cart", "login",
                   "payment", "support", "order"]
        if len(args) == 0:
            print("**class name not found**")
        elif args[0] not in classes:
            print("**class name missing**")
        elif len(args) <= 1:
            print("**instance id missing**")
        elif args[0] + "." + args[1] in objects:
            del objects[args[0] + "." + args[1]]
            storage.save()
        else:
            print("**no instance found**")

    def help_destroy(self):
        """destroy docuemntation"""
        print("Destroy an instance")

    def do_all(self, line):
        """prints all string represantation of
        all instances based on or not on the class name.
        """
        objs = []
        args = line.split()
        objects = storage.all()
        classes = ["Basemodel", "catalog", "cart", "login",
                   "payment", "support", "order"]
        if len(args) <= 0:
            for keys in objects:
                print(key)
                objs.append(objects[key].__str__())
            if len(objs) > 0:
                print(key)
        elif args[0] not in classes:
            print("**class does not exist**")
        else:
            keys = objects.keys()
            for key in keys:
                class_name = key.split(".")
                if class_name[0] == args[0]:
                    objs.append(objects[key].__str__())
                if len(objs) > 0:
                    print(objs)

    def help_all(self):
        """all documentation"""
        print("**Display all the instance of the class**")

    def do_update(self, line):
        """Updates an instance based on the class
        name and id by adding or updating attribute
        (save the change into the JSON file)
        """
        args = []
        args = shlex.split()
        objects = storage.all()
        classes = ["Basemodel", "catalog", "cart",
                   "login", "payment", "support", "order"]
        if len(args) == 0:
            print("** class name missing **")
        elif args[0] not in classes:
            print("**class does not exist**")
        elif len(args) == 1:
            print("** instance id missing **")
        elif objects.get(args[0] + "." + args[1])is None:
            print("** no instance found **")
        elif len(args) == 2:
            print("** attribute name missing **")
        elif len(args) == 3:
            print("** value missing **")
        else:
            obj = objects.get(args[0] + "." + args[1])
            setattr(obj, args[2], args[3])
            obj.save()

    def help_update(self):
        """update documentation"""
        print("Update an object fron the class")

    def do_count(self, line):
        """count the number of instances"""
        count = 0
        args = []
        args = line.split()
        instances = storage.all()
        classes = ["Basemodel", "catalog", "cart",
                   "login" "payment", "support", "order"]
        for key in instances:
            if key.split(".")[0] == args[0]:
                count += 1
            print(count)

    def help_count(self):
        """count documentation"""
        print("Count the instances number of a class")

    def emptyline(self):
        """shows the prompt when an empty line typed in
        it avoids repeating the last nonempty command entered"""
        pass

    def precmd(self, line):
        """search the commad and execute it"""
        line = line.strip()
        if re.search(r'\)', line) is None:
            return line
        line = line.replace('(', " ")
        line = line.replace(')', " ")
        if re.search(r'\{', line)and re.search(r'\}', line):
            limiter = line.find('{')
            return self.prepare_dict(line[0:limiter], line[limiter:])
        else:
            if re.search(r'\"', line):
                line = line.replace(r'\"', " ")
            return self.prepare_line(line)

    def prepare_dict(self, line, dict):
        """prepares a string to update an instance using dictionaries
        """
        import ast


    def prepare_dict(self, line, dic):
    """ prepare a string to update an instance using dictionaries """
    dic = ast.literal_eval(dic)
    if re.search(r'\"', line):
        line = line.replace('\"', "")
    if re.search(r'\.', line):
        args = line.replace('.', " ")
        args = args.split(" ")
        tmp = args[0]
        args[0] = args[1]
        args[1] = tmp
    keys = dic.keys()
    for key in keys:
        value = dic[key]
        new_line = "{} {} {} {}".format(
            args[1], args[2], str(key), str(value))
        if re.search(r'\,', new_line):
            new_line = new_line.replace(",", "")
        eval("self.do_" + args[0])(new_line)
    return ""

    def prepare_line(self, line):
        """prepares the string to return an interpretable command line"""
        if re.search(r'\.', line):
            line = line.replace('.', " ")
            line = line.split(" ")
            tmp = line[0]
            line[0] = line[1]
            line[1] = tmp
            line = " ".join(line)
        if re.search(r'\,', line):
            line = line.replace(", ", " ")
        if re.search(r'\,', line):
            line = line.replace(",", " ")
        return line


if __name__ == '__main__':
    JUMIACLONECommand().cmdloop()
