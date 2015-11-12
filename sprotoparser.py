# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function
from pypeg2 import * 

pypeg2_parse = parse #rename it,for avoiding name conflict
tag = re.compile(r"\d+")
nomeaning = blank, maybe_some(comment_sh), blank

class MainKey(str):
    grammar = "(", word, ")"

class TypeName(object):
    grammar = flag("is_arr", "*"), name()

class Filed(List):
    grammar = attr("filed", word), attr("tag", tag), ":", attr("typename", TypeName),\
            optional(MainKey), nomeaning, endl

class Struct(List):pass
class Type(List):pass

Struct.grammar = "{", nomeaning, attr("fileds", maybe_some([Filed, Type])), "}", nomeaning, endl
Type.grammar = ".", name(), attr("struct", Struct)

class Sub_pro_type(Keyword):
    grammar = Enum(K("request"), K("response"))

class Subprotocol(List):
    grammar = attr("subpro_type", Sub_pro_type), attr("pro_filed", [TypeName, Struct]), nomeaning

class Protocol(List):
    grammar = name(), attr("tag",tag), "{", nomeaning, attr("fileds", maybe_some(Subprotocol)), "}"

class Sproto(List):
    grammar = nomeaning, attr("items", maybe_some([Type, Protocol])), nomeaning
#====================================================================

class Convert:
    type_dict = {}
    protocol_dict = {}
    protocol_tags = {} #just for easiliy check

    @staticmethod
    def parse(text, name):
        obj = pypeg2_parse(text, Sproto)
        for i in obj.items:
            if hasattr(i,"tag"):
                Convert.convert_protocol(i)
            else:
                #conver all type
                Convert.convert_type(i)

        #pprint(Convert.type_dict)
        #pprint(Convert.protocol_dict)

        group = {}
        group["type"] = Convert.type_dict
        group["protocol"] = Convert.protocol_dict
        return group
    @staticmethod
    def convert_type(obj, parent_name = ""):
        type_name = obj.name
        if parent_name != "":
            type_name = parent_name + "." + obj.name
        if type_name in Convert.type_dict.keys():
            print("Error:redifine %s in type %s\n" % (i.name, i.name))
            return False
        Convert.type_dict[type_name] = Convert.convert_struct(obj.struct, type_name)

    @staticmethod
    def convert_struct(obj, name = ""):
        struct = []
        for filed in obj.fileds:
            if type(filed) == Filed:
                filed_info = {}
                filed_info["name"] = filed.filed
                filed_info["tag"] = filed.tag
                filed_info["array"] = filed.typename.is_arr
                filed_info["typename"] = filed.typename.name
                struct.append(filed_info)
            elif type(filed) == Type:
                Convert.convert_type(filed, name) 
        return struct

    @staticmethod
    def convert_protocol(obj):
        if obj.name in Convert.protocol_dict.keys():
            print("Error:redifine protocol %s\n" % obj.name)
            return
        if obj.tag in Convert.protocol_tags.keys():
            print("Error:redifine protocol tags %d" % obj.tag)
            return
        protocol = {}
        protocol["tag"] = obj.tag
        for fi in obj.fileds:
            if type(fi.pro_filed) == TypeName:
                if Convert.check_type_exists(fi.pro_filed.name):
                    protocol[fi.subpro_type] = fi.pro_filed.name
                else:
                    print("Error:non define typename %s\n" % fi.pro_filed)
                    return
            elif type(fi.pro_filed) == Struct:
                newtype_name = obj.name + "." + fi.subpro_type
                Convert.type_dict[newtype_name] = Convert.convert_struct(fi.pro_filed)
                protocol[fi.subpro_type] = newtype_name
           
        Convert.protocol_dict[obj.name] = protocol
        Convert.protocol_tags[obj.tag] = obj.tag

    @staticmethod
    def check_type_exists(name):
        if name in Convert.type_dict.keys():
            return True
        else:
            return False

def dump():
    print("to do dump")
    pass

__all__ = ["parse"]
def parse(text, name = "=text"): #name param if for compatibility of sproto lua parser, no meaning
    result = Convert.parse(text, name) 
    return result

