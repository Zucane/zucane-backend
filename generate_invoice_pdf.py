from invoice_generator import InvoiceClientConfig, InvoiceGenerator

def generate_pdf(asset_name, asset_quantity, asset_ppu_in_mxn, id_transaction_stellar):

    config = InvoiceClientConfig(api_key="sk_wPv0uwgAObGUkgpvkmcTi9WIcEcamchi")
    invoice = InvoiceGenerator(
        config=config,
        sender="Gobierno de Xochitepec.",
        to="Transportadora Ramírez S.A. de C.V.",
        logo="https://static.wixstatic.com/media/8d7c6d_0cdfaeb86c1f475cbb0e958f630abe17~mv2.png/v1/fill/w_516,h_236,al_c,q_85,usm_0.66_1.00_0.01,enc_avif,quality_auto/8d7c6d_0cdfaeb86c1f475cbb0e958f630abe17~mv2.png",
        number=id_transaction_stellar,
        notes="AHORA ERES PARTE DE LA TOKENIZACIÓN DE ACTIVOS DE CO2 DE XOCHITEPEC!",
    )

    invoice.header = "Factura de compra del token ZUCOIN"
    invoice.due_date = None
    invoice.amount_paid = asset_quantity * asset_ppu_in_mxn
    invoice.currency = "MXN"

    invoice.amount_paid_title = "Monto Pagado"
    invoice.amount_header = "Monto"
    invoice.quantity_header = "Cantidad"
    invoice.item_header = "Producto"
    invoice.unit_cost_header = "Tarifa"
    invoice.date_title = "Fecha de la Transacción"
    invoice.balance_title = "Monto Adeudado"
    invoice.to_title = "Factura Emitida a"
    invoice.tax_title = "Impuestos"
    invoice.notes_title = "¡GRACIAS!"

    invoice.invoice_number_title = "Stellar Blockchain transaction ID #"

    invoice.add_item(
        name=asset_name,
        quantity=asset_quantity,
        unit_cost=asset_ppu_in_mxn,
    )

    invoice.toggle_subtotal(shipping=False)
    pdf_path = "invoice.pdf"
    invoice.download(pdf_path)

    return pdf_path

