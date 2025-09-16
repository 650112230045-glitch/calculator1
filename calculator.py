import flet as ft
import math

# ฟังก์ชันแปลงองศาเป็นเรเดียนสำหรับ eval()
def sin_deg(d):
    return math.sin(math.radians(d))

def cos_deg(d):
    return math.cos(math.radians(d))

def tan_deg(d):
    return math.tan(math.radians(d))

def main(page: ft.Page):
    page.title = "เครื่องคิดเลข Flet"
    page.window_width = 300
    # เพิ่มความสูงเพื่อรองรับปุ่มแถวใหม่
    page.window_height = 450 

    expression = ""

    result_display = ft.Text(value="", size=24, text_align="right")

    def update_display(value):
        nonlocal expression
        expression += value
        result_display.value = expression
        page.update()

    def calculate_result(e):
        nonlocal expression
        try:
            # ใช้ locals() เพื่อให้ eval รู้จักฟังก์ชันที่เราสร้างขึ้น
            # และเปลี่ยนชื่อฟังก์ชันใน expression เพื่อให้ตรงกัน
            safe_expression = expression.replace('sin', 'sin_deg').replace('cos', 'cos_deg').replace('tan', 'tan_deg')
            
            # สร้าง dictionary ของฟังก์ชันที่ปลอดภัยสำหรับ eval
            allowed_functions = {
                'sin_deg': sin_deg,
                'cos_deg': cos_deg,
                'tan_deg': tan_deg
            }
            
            result = eval(safe_expression, {"__builtins__": None}, allowed_functions)
            expression = str(result)
        except Exception as err:
            expression = "ข้อผิดพลาด"
        result_display.value = expression
        page.update()

    def clear_display(e):
        nonlocal expression
        expression = ""
        result_display.value = ""
        page.update()

    # ปุ่มทั้งหมด (เพิ่มแถว sin, cos, tan และ .)
    buttons = [
        ["sin", "cos", "tan", "C"],
        ["7", "8", "9", "/"],
        ["4", "5", "6", "*"],
        ["1", "2", "3", "-"],
        [".", "0", "=", "+"],
    ]

    # แสดงผลลัพธ์
    page.add(
        ft.Container(
            content=result_display,
            alignment=ft.alignment.center_right,
            padding=10,
            height=70
        )
    )

    # สร้างปุ่ม
    for row in buttons:
        row_controls = []
        for btn in row:
            action = None # กำหนดค่าเริ่มต้น
            if btn == "=":
                action = calculate_result
            elif btn == "C":
                action = clear_display
            elif btn in ["sin", "cos", "tan"]:
                # สำหรับฟังก์ชันตรีโกณมิติ ให้เพิ่มวงเล็บเปิดไปด้วย
                action = lambda e, b=btn: update_display(f"{b}(")
            else:
                # สำหรับตัวเลขและเครื่องหมายอื่นๆ
                action = lambda e, b=btn: update_display(b)

            row_controls.append(
                ft.Container(
                    content=ft.ElevatedButton(text=btn, on_click=action),
                    expand=True,
                    padding=5
                )
            )
        page.add(ft.Row(controls=row_controls, expand=True))

# รันแอป
ft.app(target=main)