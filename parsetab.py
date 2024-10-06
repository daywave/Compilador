
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'AND ASIGNACION BOOLEANO BREAK COMA DISTINTO DIV ENTERO ESCRIBIR FALSO FLOTANTE FSI HACER HASTA ID IGUAL LEER LLAVDER LLAVIZQ MAYOR MAYORIGUAL MENOR MENORIGUAL MIENTRAS MULT NO NUMERO NUMERO_HEX OR PARDER PARIZQ POTENCIA PROGRAMA PUNTOCOMA RESTA SI SINO SUMA THEN VERDADERO\n    programa : PROGRAMA LLAVIZQ list_decl list_sent LLAVDER\n             | error LLAVDER\n    \n    list_decl : decl list_decl\n              | empty\n    \n    decl : tipo list_id PUNTOCOMA\n    \n    tipo : ENTERO\n         | FLOTANTE\n         | BOOLEANO\n    \n    list_id : ID COMA list_id\n            | ID\n    \n    list_sent : sent list_sent\n              | empty\n              | error PUNTOCOMA list_sent\n    \n    sent : sent_if\n         | sent_while\n         | sent_do\n         | sent_read\n         | sent_write\n         | bloque\n         | sent_assign\n         | sent_break\n    \n    sent_if : SI PARIZQ exp_bool PARDER THEN bloque FSI\n            | SI PARIZQ exp_bool PARDER THEN bloque SINO bloque FSI\n    \n    sent_while : MIENTRAS PARIZQ exp_bool PARDER bloque\n    \n    sent_do : HACER bloque HASTA PARIZQ exp_bool PARDER PUNTOCOMA\n    \n    sent_read : LEER ID PUNTOCOMA\n    \n    sent_write : ESCRIBIR exp_bool PUNTOCOMA\n    \n    bloque : LLAVIZQ list_sent LLAVDER\n    \n    sent_assign : ID ASIGNACION exp_bool PUNTOCOMA\n    \n    sent_break : BREAK PUNTOCOMA\n    \n    exp_bool : exp_bool OR comb\n             | comb\n    \n    comb : comb AND igualdad\n         | igualdad\n    \n    igualdad : igualdad IGUAL rel\n             | igualdad DISTINTO rel\n             | rel\n    \n    rel : expr MENOR expr\n        | expr MAYOR expr\n        | expr MENORIGUAL expr\n        | expr MAYORIGUAL expr\n        | expr\n    \n    expr : expr SUMA term\n         | expr RESTA term\n         | term\n    \n    term : term MULT unario\n         | term DIV unario\n         | unario\n    \n    unario : NO unario\n           | RESTA unario\n           | factor\n    \n    factor : PARIZQ exp_bool PARDER\n           | ID\n           | NUMERO\n           | VERDADERO\n           | FALSO\n    \n    empty :\n    '
    
_lr_action_items = {'PROGRAMA':([0,],[2,]),'error':([0,4,6,7,8,13,15,18,19,20,21,22,23,24,25,33,39,60,61,63,68,70,90,105,109,111,113,],[3,-57,17,-57,-4,17,17,-14,-15,-16,-17,-18,-19,-20,-21,-3,17,-30,-5,-28,-26,-27,-29,-24,-22,-25,-23,]),'$end':([1,5,37,],[0,-2,-1,]),'LLAVIZQ':([2,4,6,7,8,13,15,18,19,20,21,22,23,24,25,28,33,39,60,61,63,68,70,88,90,104,105,109,110,111,113,],[4,-57,13,-57,-4,13,13,-14,-15,-16,-17,-18,-19,-20,-21,13,-3,13,-30,-5,-28,-26,-27,13,-29,13,-24,-22,13,-25,-23,]),'LLAVDER':([3,4,6,7,8,13,14,15,16,18,19,20,21,22,23,24,25,33,36,38,39,60,61,63,64,68,70,90,105,109,111,113,],[5,-57,-57,-57,-4,-57,37,-57,-12,-14,-15,-16,-17,-18,-19,-20,-21,-3,63,-11,-57,-30,-5,-28,-13,-26,-27,-29,-24,-22,-25,-23,]),'SI':([4,6,7,8,13,15,18,19,20,21,22,23,24,25,33,39,60,61,63,68,70,90,105,109,111,113,],[-57,26,-57,-4,26,26,-14,-15,-16,-17,-18,-19,-20,-21,-3,26,-30,-5,-28,-26,-27,-29,-24,-22,-25,-23,]),'MIENTRAS':([4,6,7,8,13,15,18,19,20,21,22,23,24,25,33,39,60,61,63,68,70,90,105,109,111,113,],[-57,27,-57,-4,27,27,-14,-15,-16,-17,-18,-19,-20,-21,-3,27,-30,-5,-28,-26,-27,-29,-24,-22,-25,-23,]),'HACER':([4,6,7,8,13,15,18,19,20,21,22,23,24,25,33,39,60,61,63,68,70,90,105,109,111,113,],[-57,28,-57,-4,28,28,-14,-15,-16,-17,-18,-19,-20,-21,-3,28,-30,-5,-28,-26,-27,-29,-24,-22,-25,-23,]),'LEER':([4,6,7,8,13,15,18,19,20,21,22,23,24,25,33,39,60,61,63,68,70,90,105,109,111,113,],[-57,29,-57,-4,29,29,-14,-15,-16,-17,-18,-19,-20,-21,-3,29,-30,-5,-28,-26,-27,-29,-24,-22,-25,-23,]),'ESCRIBIR':([4,6,7,8,13,15,18,19,20,21,22,23,24,25,33,39,60,61,63,68,70,90,105,109,111,113,],[-57,31,-57,-4,31,31,-14,-15,-16,-17,-18,-19,-20,-21,-3,31,-30,-5,-28,-26,-27,-29,-24,-22,-25,-23,]),'ID':([4,6,7,8,9,10,11,12,13,15,18,19,20,21,22,23,24,25,29,31,33,39,40,41,44,51,53,55,60,61,62,63,68,70,71,72,73,74,75,76,77,78,79,80,81,82,89,90,105,109,111,113,],[-57,30,-57,-4,35,-6,-7,-8,30,30,-14,-15,-16,-17,-18,-19,-20,-21,43,56,-3,30,56,56,56,56,56,56,-30,-5,35,-28,-26,-27,56,56,56,56,56,56,56,56,56,56,56,56,56,-29,-24,-22,-25,-23,]),'BREAK':([4,6,7,8,13,15,18,19,20,21,22,23,24,25,33,39,60,61,63,68,70,90,105,109,111,113,],[-57,32,-57,-4,32,32,-14,-15,-16,-17,-18,-19,-20,-21,-3,32,-30,-5,-28,-26,-27,-29,-24,-22,-25,-23,]),'ENTERO':([4,7,61,],[10,10,-5,]),'FLOTANTE':([4,7,61,],[11,11,-5,]),'BOOLEANO':([4,7,61,],[12,12,-5,]),'PUNTOCOMA':([17,32,34,35,43,45,46,47,48,49,50,52,54,56,57,58,59,69,83,84,86,91,92,93,94,95,96,97,98,99,100,101,102,103,108,],[39,60,61,-10,68,70,-32,-34,-37,-42,-45,-48,-51,-53,-54,-55,-56,90,-50,-49,-9,-31,-33,-35,-36,-38,-39,-40,-41,-43,-44,-46,-47,-52,111,]),'PARIZQ':([26,27,31,40,41,44,51,53,55,67,71,72,73,74,75,76,77,78,79,80,81,82,89,],[40,41,55,55,55,55,55,55,55,89,55,55,55,55,55,55,55,55,55,55,55,55,55,]),'ASIGNACION':([30,],[44,]),'NO':([31,40,41,44,51,53,55,71,72,73,74,75,76,77,78,79,80,81,82,89,],[53,53,53,53,53,53,53,53,53,53,53,53,53,53,53,53,53,53,53,53,]),'RESTA':([31,40,41,44,49,50,51,52,53,54,55,56,57,58,59,71,72,73,74,75,76,77,78,79,80,81,82,83,84,89,95,96,97,98,99,100,101,102,103,],[51,51,51,51,80,-45,51,-48,51,-51,51,-53,-54,-55,-56,51,51,51,51,51,51,51,51,51,51,51,51,-50,-49,51,80,80,80,80,-43,-44,-46,-47,-52,]),'NUMERO':([31,40,41,44,51,53,55,71,72,73,74,75,76,77,78,79,80,81,82,89,],[57,57,57,57,57,57,57,57,57,57,57,57,57,57,57,57,57,57,57,57,]),'VERDADERO':([31,40,41,44,51,53,55,71,72,73,74,75,76,77,78,79,80,81,82,89,],[58,58,58,58,58,58,58,58,58,58,58,58,58,58,58,58,58,58,58,58,]),'FALSO':([31,40,41,44,51,53,55,71,72,73,74,75,76,77,78,79,80,81,82,89,],[59,59,59,59,59,59,59,59,59,59,59,59,59,59,59,59,59,59,59,59,]),'COMA':([35,],[62,]),'HASTA':([42,63,],[67,-28,]),'OR':([45,46,47,48,49,50,52,54,56,57,58,59,65,66,69,83,84,85,91,92,93,94,95,96,97,98,99,100,101,102,103,106,],[71,-32,-34,-37,-42,-45,-48,-51,-53,-54,-55,-56,71,71,71,-50,-49,71,-31,-33,-35,-36,-38,-39,-40,-41,-43,-44,-46,-47,-52,71,]),'PARDER':([46,47,48,49,50,52,54,56,57,58,59,65,66,83,84,85,91,92,93,94,95,96,97,98,99,100,101,102,103,106,],[-32,-34,-37,-42,-45,-48,-51,-53,-54,-55,-56,87,88,-50,-49,103,-31,-33,-35,-36,-38,-39,-40,-41,-43,-44,-46,-47,-52,108,]),'AND':([46,47,48,49,50,52,54,56,57,58,59,83,84,91,92,93,94,95,96,97,98,99,100,101,102,103,],[72,-34,-37,-42,-45,-48,-51,-53,-54,-55,-56,-50,-49,72,-33,-35,-36,-38,-39,-40,-41,-43,-44,-46,-47,-52,]),'IGUAL':([47,48,49,50,52,54,56,57,58,59,83,84,92,93,94,95,96,97,98,99,100,101,102,103,],[73,-37,-42,-45,-48,-51,-53,-54,-55,-56,-50,-49,73,-35,-36,-38,-39,-40,-41,-43,-44,-46,-47,-52,]),'DISTINTO':([47,48,49,50,52,54,56,57,58,59,83,84,92,93,94,95,96,97,98,99,100,101,102,103,],[74,-37,-42,-45,-48,-51,-53,-54,-55,-56,-50,-49,74,-35,-36,-38,-39,-40,-41,-43,-44,-46,-47,-52,]),'MENOR':([49,50,52,54,56,57,58,59,83,84,99,100,101,102,103,],[75,-45,-48,-51,-53,-54,-55,-56,-50,-49,-43,-44,-46,-47,-52,]),'MAYOR':([49,50,52,54,56,57,58,59,83,84,99,100,101,102,103,],[76,-45,-48,-51,-53,-54,-55,-56,-50,-49,-43,-44,-46,-47,-52,]),'MENORIGUAL':([49,50,52,54,56,57,58,59,83,84,99,100,101,102,103,],[77,-45,-48,-51,-53,-54,-55,-56,-50,-49,-43,-44,-46,-47,-52,]),'MAYORIGUAL':([49,50,52,54,56,57,58,59,83,84,99,100,101,102,103,],[78,-45,-48,-51,-53,-54,-55,-56,-50,-49,-43,-44,-46,-47,-52,]),'SUMA':([49,50,52,54,56,57,58,59,83,84,95,96,97,98,99,100,101,102,103,],[79,-45,-48,-51,-53,-54,-55,-56,-50,-49,79,79,79,79,-43,-44,-46,-47,-52,]),'MULT':([50,52,54,56,57,58,59,83,84,99,100,101,102,103,],[81,-48,-51,-53,-54,-55,-56,-50,-49,81,81,-46,-47,-52,]),'DIV':([50,52,54,56,57,58,59,83,84,99,100,101,102,103,],[82,-48,-51,-53,-54,-55,-56,-50,-49,82,82,-46,-47,-52,]),'FSI':([63,107,112,],[-28,109,113,]),'SINO':([63,107,],[-28,110,]),'THEN':([87,],[104,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'programa':([0,],[1,]),'list_decl':([4,7,],[6,33,]),'decl':([4,7,],[7,7,]),'empty':([4,6,7,13,15,39,],[8,16,8,16,16,16,]),'tipo':([4,7,],[9,9,]),'list_sent':([6,13,15,39,],[14,36,38,64,]),'sent':([6,13,15,39,],[15,15,15,15,]),'sent_if':([6,13,15,39,],[18,18,18,18,]),'sent_while':([6,13,15,39,],[19,19,19,19,]),'sent_do':([6,13,15,39,],[20,20,20,20,]),'sent_read':([6,13,15,39,],[21,21,21,21,]),'sent_write':([6,13,15,39,],[22,22,22,22,]),'bloque':([6,13,15,28,39,88,104,110,],[23,23,23,42,23,105,107,112,]),'sent_assign':([6,13,15,39,],[24,24,24,24,]),'sent_break':([6,13,15,39,],[25,25,25,25,]),'list_id':([9,62,],[34,86,]),'exp_bool':([31,40,41,44,55,89,],[45,65,66,69,85,106,]),'comb':([31,40,41,44,55,71,89,],[46,46,46,46,46,91,46,]),'igualdad':([31,40,41,44,55,71,72,89,],[47,47,47,47,47,47,92,47,]),'rel':([31,40,41,44,55,71,72,73,74,89,],[48,48,48,48,48,48,48,93,94,48,]),'expr':([31,40,41,44,55,71,72,73,74,75,76,77,78,89,],[49,49,49,49,49,49,49,49,49,95,96,97,98,49,]),'term':([31,40,41,44,55,71,72,73,74,75,76,77,78,79,80,89,],[50,50,50,50,50,50,50,50,50,50,50,50,50,99,100,50,]),'unario':([31,40,41,44,51,53,55,71,72,73,74,75,76,77,78,79,80,81,82,89,],[52,52,52,52,83,84,52,52,52,52,52,52,52,52,52,52,52,101,102,52,]),'factor':([31,40,41,44,51,53,55,71,72,73,74,75,76,77,78,79,80,81,82,89,],[54,54,54,54,54,54,54,54,54,54,54,54,54,54,54,54,54,54,54,54,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> programa","S'",1,None,None,None),
  ('programa -> PROGRAMA LLAVIZQ list_decl list_sent LLAVDER','programa',5,'p_programa','sintactico.py',7),
  ('programa -> error LLAVDER','programa',2,'p_programa','sintactico.py',8),
  ('list_decl -> decl list_decl','list_decl',2,'p_list_decl','sintactico.py',17),
  ('list_decl -> empty','list_decl',1,'p_list_decl','sintactico.py',18),
  ('decl -> tipo list_id PUNTOCOMA','decl',3,'p_decl','sintactico.py',27),
  ('tipo -> ENTERO','tipo',1,'p_tipo','sintactico.py',33),
  ('tipo -> FLOTANTE','tipo',1,'p_tipo','sintactico.py',34),
  ('tipo -> BOOLEANO','tipo',1,'p_tipo','sintactico.py',35),
  ('list_id -> ID COMA list_id','list_id',3,'p_list_id','sintactico.py',41),
  ('list_id -> ID','list_id',1,'p_list_id','sintactico.py',42),
  ('list_sent -> sent list_sent','list_sent',2,'p_list_sent','sintactico.py',51),
  ('list_sent -> empty','list_sent',1,'p_list_sent','sintactico.py',52),
  ('list_sent -> error PUNTOCOMA list_sent','list_sent',3,'p_list_sent','sintactico.py',53),
  ('sent -> sent_if','sent',1,'p_sent','sintactico.py',65),
  ('sent -> sent_while','sent',1,'p_sent','sintactico.py',66),
  ('sent -> sent_do','sent',1,'p_sent','sintactico.py',67),
  ('sent -> sent_read','sent',1,'p_sent','sintactico.py',68),
  ('sent -> sent_write','sent',1,'p_sent','sintactico.py',69),
  ('sent -> bloque','sent',1,'p_sent','sintactico.py',70),
  ('sent -> sent_assign','sent',1,'p_sent','sintactico.py',71),
  ('sent -> sent_break','sent',1,'p_sent','sintactico.py',72),
  ('sent_if -> SI PARIZQ exp_bool PARDER THEN bloque FSI','sent_if',7,'p_sent_if','sintactico.py',78),
  ('sent_if -> SI PARIZQ exp_bool PARDER THEN bloque SINO bloque FSI','sent_if',9,'p_sent_if','sintactico.py',79),
  ('sent_while -> MIENTRAS PARIZQ exp_bool PARDER bloque','sent_while',5,'p_sent_while','sintactico.py',88),
  ('sent_do -> HACER bloque HASTA PARIZQ exp_bool PARDER PUNTOCOMA','sent_do',7,'p_sent_do','sintactico.py',94),
  ('sent_read -> LEER ID PUNTOCOMA','sent_read',3,'p_sent_read','sintactico.py',100),
  ('sent_write -> ESCRIBIR exp_bool PUNTOCOMA','sent_write',3,'p_sent_write','sintactico.py',106),
  ('bloque -> LLAVIZQ list_sent LLAVDER','bloque',3,'p_bloque','sintactico.py',112),
  ('sent_assign -> ID ASIGNACION exp_bool PUNTOCOMA','sent_assign',4,'p_sent_assign','sintactico.py',118),
  ('sent_break -> BREAK PUNTOCOMA','sent_break',2,'p_sent_break','sintactico.py',124),
  ('exp_bool -> exp_bool OR comb','exp_bool',3,'p_exp_bool','sintactico.py',130),
  ('exp_bool -> comb','exp_bool',1,'p_exp_bool','sintactico.py',131),
  ('comb -> comb AND igualdad','comb',3,'p_comb','sintactico.py',140),
  ('comb -> igualdad','comb',1,'p_comb','sintactico.py',141),
  ('igualdad -> igualdad IGUAL rel','igualdad',3,'p_igualdad','sintactico.py',150),
  ('igualdad -> igualdad DISTINTO rel','igualdad',3,'p_igualdad','sintactico.py',151),
  ('igualdad -> rel','igualdad',1,'p_igualdad','sintactico.py',152),
  ('rel -> expr MENOR expr','rel',3,'p_rel','sintactico.py',164),
  ('rel -> expr MAYOR expr','rel',3,'p_rel','sintactico.py',165),
  ('rel -> expr MENORIGUAL expr','rel',3,'p_rel','sintactico.py',166),
  ('rel -> expr MAYORIGUAL expr','rel',3,'p_rel','sintactico.py',167),
  ('rel -> expr','rel',1,'p_rel','sintactico.py',168),
  ('expr -> expr SUMA term','expr',3,'p_expr','sintactico.py',177),
  ('expr -> expr RESTA term','expr',3,'p_expr','sintactico.py',178),
  ('expr -> term','expr',1,'p_expr','sintactico.py',179),
  ('term -> term MULT unario','term',3,'p_term','sintactico.py',191),
  ('term -> term DIV unario','term',3,'p_term','sintactico.py',192),
  ('term -> unario','term',1,'p_term','sintactico.py',193),
  ('unario -> NO unario','unario',2,'p_unario','sintactico.py',205),
  ('unario -> RESTA unario','unario',2,'p_unario','sintactico.py',206),
  ('unario -> factor','unario',1,'p_unario','sintactico.py',207),
  ('factor -> PARIZQ exp_bool PARDER','factor',3,'p_factor','sintactico.py',219),
  ('factor -> ID','factor',1,'p_factor','sintactico.py',220),
  ('factor -> NUMERO','factor',1,'p_factor','sintactico.py',221),
  ('factor -> VERDADERO','factor',1,'p_factor','sintactico.py',222),
  ('factor -> FALSO','factor',1,'p_factor','sintactico.py',223),
  ('empty -> <empty>','empty',0,'p_empty','sintactico.py',232),
]
