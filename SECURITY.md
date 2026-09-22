# Política de seguridad

Este repositorio contiene una especificación y el pipeline que la publica, no software en ejecución. Aun así, hay hallazgos que conviene reportar de forma privada antes de que sean públicos, porque quien ya siguió la guía queda expuesto mientras tanto.

## Qué reportar aquí

1. **Defectos de la especificación con impacto de seguridad.** Una recomendación cuyo cumplimiento debilitaría la seguridad de una implementación, por ejemplo en la autenticación, la autorización, el consentimiento o la auditoría.
2. **Datos expuestos en el material publicado.** Ejemplos, diagramas o textos que contengan datos personales, credenciales o endpoints internos reales.
3. **El sitio y su cadena de publicación.** Problemas en los flujos de trabajo de `.github/workflows`, en los guiones de `_scripts` o en el sitio que se despliega a partir de ellos.

## Qué no corresponde a este repositorio

Las vulnerabilidades de los sistemas que implementan esta guía, y las de los servidores FHIR y demás software de terceros, deben reportarse a quien opera ese software. Aquí solo se atiende lo que esta especificación dice y lo que este repositorio publica.

## Cómo reportar

Use «Report a vulnerability» en la pestaña Security de este repositorio, o escriba a [juan@meddyg.com](mailto:juan@meddyg.com). No abra un issue público, porque eso divulga el problema a quienes aún no pueden corregirlo. Describa el hallazgo, indique la página, la sección o el archivo afectado y explique qué haría posible el problema. Se acusa recibo en un plazo máximo de cinco días hábiles.

Los reportes sobre el comportamiento de las personas de la comunidad no van por esta vía, sino por la que describe el [Código de Conducta](CODE_OF_CONDUCT.md).
