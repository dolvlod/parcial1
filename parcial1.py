import uctypes
from machine import mem32
import array

def read_points():
    # Creamos un array de 8 floats: [x0, y0, x1, y1, x2, y2, x3, y3]
    pts = array.array('f', [0.0] * 8)
    for i in range(4):
        x = float(input(f'Ingrese x{i}: '))
        y = float(input(f'Ingrese y{i}: '))
        pts[2*i]   = x
        pts[2*i+1] = y
    return pts

def bezier_cubic(points, steps=4):
    n = steps + 1
    # Array de salida con 2 coordenadas por cada uno de los n puntos
    res = array.array('f', [0.0] * (2 * n))
    for i in range(n):
        t = i / steps
        u = 1 - t
        # coeficientes de Bernstein
        b0 = u*u*u
        b1 = 3*u*u*t
        b2 = 3*u*t*t
        b3 = t*t*t

        # calculamos x, y
        res[2*i]   = b0*points[0] + b1*points[2] + b2*points[4] + b3*points[6]
        res[2*i+1] = b0*points[1] + b1*points[3] + b2*points[5] + b3*points[7]
    return res

def main():
    pts = read_points()
    result = bezier_cubic(pts, steps=5)

    print('\nCoordenadas de la curva Bézier (5 puntos):')
    for i in range(5):
        x, y = result[2*i], result[2*i+1]
        print(f' t={i}/4 → ({x:.3f}, {y:.3f})')

    # Leemos los bits crudos del primer float (x0) usando mem32.
    # Primero obtenemos la dirección de inicio del buffer del array:
    addr = uctypes.addressof(result)
    word0 = mem32[addr // 4]
    print(f'\nPrimer valor en mem32 (bits de x0): 0x{word0:08X}')

if __name__ == '__main__':
    main()
