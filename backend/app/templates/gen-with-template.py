from weasyprint import HTML

HTML('invoice_template.html').write_pdf('output.pdf')