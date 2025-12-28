<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
  <xsl:template match="/">
    <html>
      <body>
        <ul>
          <li><b>Vendor:</b> <xsl:value-of select="system-property('xsl:vendor')"/></li>
          <li><b>Vendor URL:</b> <xsl:value-of select="system-property('xsl:vendor-url')"/></li>
          <li><b>Version:</b> <xsl:value-of select="system-property('xsl:version')"/></li>
        </ul>
      </body>
    </html>
  </xsl:template>
</xsl:stylesheet>
