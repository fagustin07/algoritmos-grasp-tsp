import xml.etree.ElementTree as ET

def crear_grafo_desde(file):
    tree = ET.parse(file)
    root = tree.getroot()

    grafo = root.find('graph')
    nodos = grafo.findall('vertex')

    V = []
    X = {}

    for i,v in enumerate(nodos):
        V.append(i)
        aristas = v.findall('edge')
        X[i,i] = 0
        for e in aristas:
            costo = float(e.attrib.get('cost'))
            X[i, int(e.text)] = costo
    
    return (V, X)