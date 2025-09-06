import streamlit as st
import qrcode
from io import BytesIO

def generate_upi_qr(upi_id, amount = ""):
  upi_url = f"upi://pay?pa={upi_id}"
  if amount.strip():
    upi_url += f"&am={amount}&cu=INR"

  qr = qrcode.make(upi_url)

  buf = BytesIO()
  qr.save(buf, format="PNG")
  byte_im = buf.getvalue()

  return byte_im, upi_url

st.set_page_config(page_title="PayQR", page_icon="💳", layout="centered")

st.title("💳 PayQR")
st.write("Generates a UPI QR code that works with **GPay, PhonePe, Paytm** etc.")

upi_id = st.text_input("Enter the UPI ID")
amount = st.text_input("Enter Amount(Optional)")

if st.button("Generate QR Code"):
  if not upi_id.strip():
    st.warning("Please Enter the UPI ID before generating QR")
  else:
    try:
      byte_im, upi_url = generate_upi_qr(upi_id, amount)

      st.image(byte_im, caption="Scan this QR code to pay")

      st.download_button(
        label="Download QR Code",
        data = byte_im,
        file_name = f"{upi_id}_qr.png",
        mime = "image/png"
      )

      st.success("QR Code generated Successfully")
      st.code(upi_url, language="text")

    except Exception as e:
      st.error(f"{str(e)}")

