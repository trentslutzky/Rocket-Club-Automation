import weasyprint

pdf = weasyprint.HTML('http://192.168.1.80:5000/resume/4405').write_pdf('out.pdf')
