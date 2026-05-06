<?xml version="1.1" encoding="UTF-8" ?>
<xsl:stylesheet xmlns="index-documents:1" xpath-default-namespace="index-documents:1" xmlns:stroom="stroom" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" version="2.0">
   <xsl:template match="document">
     
     <xsl:copy>
      <field>
        <name>StreamId</name>
        <type>Id</type>
        <indexed>true</indexed>
        <stored>true</stored>
        <value><xsl:value-of select="@StreamId"/></value>
      </field>
      
      <field>
        <name>EventId</name>
        <type>Id</type>
        <indexed>true</indexed>
        <stored>true</stored>
        <value><xsl:value-of select="@EventId"/></value>
      </field>
      
      <xsl:apply-templates select="node()"/>
     </xsl:copy>
  </xsl:template>
  
   <xsl:template match="node()|@*">
     <xsl:copy>
      <xsl:apply-templates select="node()|@*"/>
     </xsl:copy>
  </xsl:template>
</xsl:stylesheet>
