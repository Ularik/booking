from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
)
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


def generate_pdf(bookings: list[dict], filename="media/bookings.pdf"):
    pdfmetrics.registerFont(
        TTFont("DejaVuSans", "media/fonts/DejaVuSans.ttf")
    )

    styles = getSampleStyleSheet()

    for style_name in styles.byName:
        styles[style_name].fontName = "DejaVuSans"

    doc = SimpleDocTemplate(filename)

    elements = []

    for booking in bookings:
        elements.extend(
            [
                Paragraph(
                    f"<b>Бронирование №{booking['id']}</b>",
                    styles["Title"],
                ),
                Spacer(1, 10),

                Paragraph(
                    f"<b>Комната:</b> {booking['room_id']}",
                    styles["Normal"],
                ),
                Paragraph(
                    f"<b>Пользователь:</b> {booking['user_id']}",
                    styles["Normal"],
                ),
                Paragraph(
                    f"<b>Дата заезда:</b> "
                    f"{booking['from_date'].strftime('%d.%m.%Y')}",
                    styles["Normal"],
                ),
                Paragraph(
                    f"<b>Дата выезда:</b> "
                    f"{booking['to_date'].strftime('%d.%m.%Y')}",
                    styles["Normal"],
                ),
                Paragraph(
                    f"<b>Стоимость:</b> {booking['price']} сом",
                    styles["Normal"],
                ),
                Paragraph(
                    f"<b>Статус:</b> {booking['status']}",
                    styles["Normal"],
                ),
                Paragraph(
                    f"<b>Оплачено:</b> "
                    f"{'Да' if booking['is_paid'] else 'Нет'}",
                    styles["Normal"],
                ),
                Paragraph(
                    f"<b>Дата создания:</b> "
                    f"{booking['created_at'].strftime('%d.%m.%Y %H:%M')}",
                    styles["Normal"],
                ),
                Spacer(1, 20),
                Paragraph(
                    "_" * 100,
                    styles["Normal"],
                ),
                Spacer(1, 20),
            ]
        )

    doc.build(elements)

    return filename