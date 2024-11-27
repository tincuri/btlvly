#Import libraries
import numpy as np
import sympy as sp
import matplotlib.pyplot as plt
#Khai biến
x, y, t, v0, alpha1, alpha2, g = sp.symbols("x y t v_0 alpha_1 alpha_2 g")

#Giải phương trình và trả về kết quả khác một số được chọn 
def solve(eq, var, excluded_sol):
    solutions = sp.solve(eq,var)
    return solutions[0] if round(float(solutions[0]), 2) != round(float(excluded_sol), 2) else solutions[1]

#Vận tốc ban đầu và gia tốc của hai phương
vx0 = v0*sp.cos(alpha1)
vy0 = v0*sp.sin(alpha1)
ax = 0
ay = -g

#Vận tốc và tọa độ của phương x và y theo thời gian
vy_t = vy0 + sp.integrate(ay,t)
vx_t = vx0 + sp.integrate(ax,t)
x_t = sp.integrate(vx_t,t)
y_t = sp.integrate(vy_t,t)

#Tìm thời điểm chạm đất
T = solve(y_t, t, 0) #Giải y_t = 0 và tìm t lúc đó    

#Quãng đường theo phương x đi được, gọi khoảng cách này là L1
L1 = sp.simplify(x_t.subs(t, T))
#Tương tự, ta có khoảng cách L2 của góc ném 2 là khi thế alpha1 với alpha2
L2 = L1.subs(alpha1, alpha2)

#Đặt L1 = L2 và tìm alpha2 theo alpha1
alpha2eq = sp.solve(L1-L2, alpha2)

#Nhập input
while True:
    alpha1_input = float(input("Nhập alpha1: "))
    if 0 < alpha1_input < np.pi:#Bắt trường hợp lỗi
        break
    print("Góc không hợp lệ, vui lòng nhập lại.")
#Đổi từ độ sang rad
v0_input = float(input("Nhập v0: "))

#Tính giá trị của alpha2
if alpha1_input < np.pi/2:
    L1num=L1.subs(alpha1, alpha1_input)    
    a2 = solve(L1num - L2, alpha2, alpha1_input)
elif alpha1_input == np.pi/2 : #Bắt trường hợp pi/2
    a2 = alpha1_input
else: #Bắt trường hợp alpha1 > pi/2
    L1num=L1.subs(alpha1, np.pi - alpha1_input)
    a2 = np.pi - solve(L1num - L2, alpha2, np.pi - alpha1_input)

#print phương trình và kết quả:
print(f" Phương trình của alpha_2 theo alpha_1 là: \n {alpha2eq[0]} khi alpha1 < 45 \nvà {alpha2eq[1]} khi alpha1 > 45 \n\n Kết quả số là: {a2}")

#Thế các biến. T1, T2 lần lượt là thời gian chạm đất của 2 quỹ đạo
T1 = float(T.subs([(g, 9.81), (v0, v0_input), (alpha1, alpha1_input)]))
T2 = float(T.subs([(g, 9.81), (v0, v0_input), (alpha1, a2)]))

#Thế các biến cho 2 hàm
y_t1 = y_t.subs([(g, 9.81), (v0, v0_input), (alpha1, alpha1_input)])
x_t1 = x_t.subs([(g, 9.81), (v0, v0_input), (alpha1, alpha1_input)])
y_t2 = y_t.subs([(g, 9.81), (v0, v0_input), (alpha1, a2)])
x_t2 = x_t.subs([(g, 9.81), (v0, v0_input), (alpha1, a2)])

#Chuyển các hàm sympy về các hàm numpy có thể thế số
x1 = sp.lambdify(t, x_t1, 'numpy')
y1 = sp.lambdify(t, y_t1, 'numpy')
x2 = sp.lambdify(t, x_t2, 'numpy')
y2 = sp.lambdify(t, y_t2, 'numpy')

# Plot hai hàm
t1 = np.linspace(0, T1, 100)
t2 = np.linspace(0, T2, 100)
plt.plot(x1(t1), y1(t1), label='Góc ném 1')
plt.plot(x2(t2), y2(t2), label='Góc ném 2')
plt.xlabel('x(t)')
plt.ylabel('y(t)')
plt.title('Hai quỹ đạo tương ứng với hai góc ném')
plt.legend() #Thêm legend
plt.axis('equal') # Chỉnh tỉ lệ hai trục giống nhau
plt.grid(True)
plt.show()
