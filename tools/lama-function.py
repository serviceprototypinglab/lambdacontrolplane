import os
import re

class QueryObject:
    def __init__(self, subexpressions, tablename, wherecolumn, whereoperator, wherevalue, ordercolumn, orderdirection, distinct):
        self.subexpressions = subexpressions
        self.tablename = tablename
        self.wherecolumn = wherecolumn
        self.whereoperator = whereoperator
        self.wherevalue = wherevalue
        self.ordercolumn = ordercolumn
        self.orderdirection = orderdirection
        self.distinct = distinct

    def __str__(self):
        return "QO{%s/%s}" % (self.tablename, str(self.subexpressions))

def selectionexpression(s):
    try:
        from math import sin, cos, tan, sqrt
        result = eval(s, {"__builtins__": None, "sin": sin, "cos": cos, "tan": tan, "sqrt": sqrt, "abs": abs, "round": round, "lower": str.lower, "upper": str.upper, "length": len}, {})
        return str(result)
    except:
        return None

def getentries(tablename, colname):
    entries = os.getenv("C" + colname.upper())
    if entries:
        return entries.split(";")
    else:
        return []

def getcolumns(tablename):
    return [x.lower() for x in os.getenv("T" + tablename.upper()).split(";")]

def execute(tables, qo):
    allentries = {}
    tablecolumns = None
    if qo.tablename:
        tablecolumns = getcolumns(qo.tablename)
    for subexpression in qo.subexpressions:
        subexpression = subexpression.replace(",", "")
        value = selectionexpression(subexpression)
        if value:
            allentries[subexpression] = [value]
            continue
        if not qo.tablename:
            raise Exception("Expression %s requires table specification." % subexpression)
        if subexpression == "count(*)":
            allentries[subexpression] = [999]
        elif subexpression == "*" or subexpression in tablecolumns:
            selectedcolumns = [subexpression]
            if subexpression == "*":
                selectedcolumns = tablecolumns
            for colname in selectedcolumns:
                #column = table.columns[colname]
                #self.outputdata("Column %s [%s]:" % (colname, column.coltype))
                if qo.ordercolumn == colname:
                    #entries = column.getentriessorted(orderdirection)
                    allentries["???"] = [23]
                else:
                    if qo.wherecolumn == colname or qo.distinct:
                        #entries = column.getentries(whereoperator, wherevalue, distinct)
                        allentries["???"] = [42]
                    else:
                        # entries = column.getentries()
                        entries = getentries(qo.tablename, colname)
                        allentries[colname] = entries
        else:
            notapplied = 0
            for colname in tablecolumns:
                if subexpression == "sum(" + colname + ")":
                    expr = sum([int(x) for x in getentries(qo.tablename, colname)])
                    allentries[subexpression] = [expr]
                else:
                    # ...
                    notapplied += 1
                if notapplied == len(tablecolumns):
                    raise Exception("Unhandled query part: " + subexpression)
    return allentries

def extre(s):
    r_sub = re.compile(" ([^\*])")
    exts = r_sub.sub(" +\\1", s) + "$"
    return exts

def runquery(tables, q):
    r_select = re.compile(extre("SELECT (?:(DISTINCT) )?((?:(?:\S+)(?:, *)?)+)(?: FROM (\S+))?(?: WHERE (\S+) (=|<|>|<>|<=|>=|(?:NOT )?LIKE) (\S+))?(?: ORDER BY (\S+)(?: (ASC|DESC))?)?"))

    m_select = r_select.match(q)
    if m_select:
        tablename = None
        wherecolumn = None
        whereoperator = None
        wherevalue = None
        ordercolumn = None
        orderdirection = None
        distinct = None
        if m_select.group(1) != None:
            distinct = m_select.group(1).lower()
        if m_select.group(3) != None:
            tablename = m_select.group(3).lower()
        if m_select.group(4) != None:
            wherecolumn = m_select.group(4).lower()
        if m_select.group(5) != None:
            whereoperator = m_select.group(5).lower()
        if m_select.group(6) != None:
            wherevalue = m_select.group(6).lower()
        if m_select.group(7) != None:
            ordercolumn = m_select.group(7).lower()
        if m_select.group(8) != None:
            orderdirection = m_select.group(8)
        if tablename and not tablename in tables:
            raise Exception("Non-existing table %s." % tablename)

        p_subexpressions = m_select.group(2).lower()
        r_subexpressions = re.compile("(\S+)(?:, )?")
        subexpressions = r_subexpressions.findall(p_subexpressions)

        if tablename:
            qo = QueryObject(subexpressions, tablename, wherecolumn, whereoperator, wherevalue, ordercolumn, orderdirection, distinct)

            return execute(tables, qo)
    else:
        raise Exception("Not a query.")
        
def gettables():
    tables = {}
    try:
        tablenames = [x.lower() for x in os.getenv("DT").split(";")]
        for tablename in tablenames:
            tables[tablename] = getcolumns(tablename)
    except:
        pass
    return tables

def lambda_handler(event, context):
    if "query" in event:
        query = event["query"]
        #res = os.getenv("CA")
        tables = gettables()
        res = runquery(tables, query);
    elif "admin" in event:
        if event["admin"] == "tables":
            res = gettables()
        else:
            raise Exception("Unknown administration command.")
    else:
        raise Exception("No command given.")
    return res
