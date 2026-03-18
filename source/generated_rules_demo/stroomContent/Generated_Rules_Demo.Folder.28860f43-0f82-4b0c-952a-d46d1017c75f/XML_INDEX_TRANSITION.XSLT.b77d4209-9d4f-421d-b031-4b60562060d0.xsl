<?xml version="1.1" encoding="UTF-8" ?>
<xsl:stylesheet xmlns="index-documents:1" xpath-default-namespace="http://schemas.microsoft.com/win/2004/08/events/event" xmlns:stroom="stroom" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" version="2.0">
  <xsl:template match="/">
    <index-documents xmlns="index-documents:1" xsi:schemaLocation="index-documents:1 file://index-documents-v1.0.xsd" version="1.0">
      <xsl:apply-templates />
    </index-documents>
  </xsl:template>
  <xsl:template match="Event">
    <document>
      <xsl:apply-templates mode="path" />
    </document>
  </xsl:template>

  <!-- Main path building template -->
  <xsl:template match="*" mode="path">
    <xsl:param name="prefix" select="''" />

    <!-- Build current path -->
    <xsl:variable name="current-path">
      <xsl:choose>
        <xsl:when test="$prefix != ''">
          <xsl:value-of select="concat($prefix, '.', local-name())" />
        </xsl:when>
        <xsl:otherwise>
          <xsl:value-of select="local-name()" />
        </xsl:otherwise>
      </xsl:choose>
    </xsl:variable>

    <!-- Handle elements with text content (leaf nodes) -->
    <xsl:choose>

      <!-- Special handling for EventData/Data elements with Name attribute -->
      <xsl:when test="local-name() = 'Data' and @Name">
        <field>
          <name>
            <xsl:value-of select="concat($prefix, '.', @Name)" />
          </name>
          <type>Text</type>
          <indexed>true</indexed>
          <stored>true</stored>
          <value>
            <xsl:value-of select="translate(normalize-space(text()), '&quot;', '')" />
          </value>
        </field>
      </xsl:when>

      <!-- Elements with only text content (no child elements) -->
      <xsl:when test="not(*) and normalize-space(text()) != ''">
        <field>
          <name>
            <xsl:value-of select="$current-path" />
          </name>
          <type>Text</type>
          <indexed>true</indexed>
          <stored>true</stored>
          <value>
            <xsl:value-of select="translate(normalize-space(text()), '&quot;', '')" />
          </value>
        </field>
        <xsl:text>&#10;</xsl:text>
      </xsl:when>
    </xsl:choose>

    <!-- Output attributes -->
    <xsl:for-each select="@*">

      <!-- Skip Name attribute for Data elements (already handled above) -->
      <xsl:if test="not(local-name() = 'Name' and local-name(..) = 'Data')">
        <field>
          <name>
            <xsl:value-of select="concat($current-path, '.@', local-name())" />
          </name>
          <type>Text</type>
          <indexed>true</indexed>
          <stored>true</stored>
          <value>
            <xsl:value-of select="." />
          </value>
        </field>
      </xsl:if>
    </xsl:for-each>

    <!-- Recurse into child elements -->
    <xsl:apply-templates select="*" mode="path">
      <xsl:with-param name="prefix" select="$current-path" />
    </xsl:apply-templates>
  </xsl:template>
</xsl:stylesheet>
