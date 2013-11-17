<?xml version="1.0"?>

<xsl:stylesheet version="1.0"
xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:abbyy="http://www.abbyy.com/FineReader_xml/FineReader8-schema-v2.xml">

<xsl:template match="abbyy:document">
    <html>
        <head>
            <meta name='ocr-id' value='abbyy' />
            <meta name='ocr-recognized' value='lines text' />
        </head>
    <body>
        <xsl:for-each select="abbyy:page">
            <xsl:variable name="pagewidth"><xsl:value-of select="@width" /></xsl:variable>                
            <xsl:variable name="pageheight"><xsl:value-of select="@height" /></xsl:variable>
            <xsl:variable name="pageId"><xsl:number from="/" level="any" count="abbyy:page" /></xsl:variable>
            
            <div class="ocr_page" id="page_{$pageId}" title="bbox 0 0 {$pagewidth} {$pageheight}">
            <xsl:for-each select="abbyy:block[@blockType='Text']">
                <xsl:variable name="x0"><xsl:value-of select="@l" /></xsl:variable>                
                <xsl:variable name="y0"><xsl:value-of select="@t" /></xsl:variable>
                <xsl:variable name="x1"><xsl:value-of select="@r" /></xsl:variable>                
                <xsl:variable name="y1"><xsl:value-of select="@b" /></xsl:variable>

                <div class="ocr_carea" title="bbox {$x0} {$y0} {$x1} {$y1}">
                <xsl:for-each select="abbyy:text/abbyy:par">
                    <p>
                    <xsl:for-each select="abbyy:line">
                        <xsl:variable name="lineId"><xsl:number from="/" level="any" count="abbyy:line" /></xsl:variable>
                        <xsl:variable name="lx0"><xsl:value-of select="@l" /></xsl:variable>                
                        <xsl:variable name="ly0"><xsl:value-of select="@t" /></xsl:variable>
                        <xsl:variable name="lx1"><xsl:value-of select="@r" /></xsl:variable>                
                        <xsl:variable name="ly1"><xsl:value-of select="@b" /></xsl:variable>
                        <span class="ocr_line" id="line_{$lineId}" title="bbox {$lx0} {$ly0} {$lx1} {$ly1}">
                            <xsl:value-of select="." />
                            <!--<xsl:variable name="xBoxes">
                                <xsl:value-of separator=" " select="(*[@l]|*[@t]|*[@r]|*[@b])[text()]" />
                            </xsl:variable>
                            <span class="ocr_cinfo" title="x_boxes {$xBoxes}"></span>-->
                        </span>  
                    </xsl:for-each>
                    </p>
                </xsl:for-each>
                </div>
            </xsl:for-each>
            </div>
        </xsl:for-each>
    </body>
    </html>
</xsl:template>

</xsl:stylesheet>

