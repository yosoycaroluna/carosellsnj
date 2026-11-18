# Ajustes posteriores a build.py: textos que no afirman un guardado sin confirmacion tecnica.
import sys, os
P_ = os.path.join(sys.argv[1], "_next/static/chunks/page-cPYjA9V1.js")
j = open(P_, encoding="utf-8").read()
R = [
 ("Your request has been saved. Download your guide below and keep it handy.", "Your request was sent. Download your guide below and keep it handy."),
 ("Tu solicitud está guardada. Descarga la guía y tenla a mano.", "Tu solicitud fue enviada. Descarga la guía y tenla a mano."),
 ("Your request and contact details are saved so Carolina can follow up about your real estate needs.", "Your request and contact details are sent to Carolina’s private form so she can follow up about your real estate needs."),
 ("Tu solicitud y tus datos se guardan para que Carolina pueda dar seguimiento.", "Tu solicitud y tus datos se envían al formulario privado de Carolina para que pueda dar seguimiento."),
]
for old, new in R:
    if j.count(old) != 1: raise SystemExit("AJUSTE FAILED: " + old[:60])
    j = j.replace(old, new)
open(P_, "w", encoding="utf-8").write(j)
print("AJUSTES OK")
