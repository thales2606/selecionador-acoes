from pandas._libs.missing import NA


class Filtros:
    def aplicar_filtros(self, df):
        df = self.retirar_bdrs(df)
        df = self.retirar_duplicados_mantendo_maior_volume_financeiro(df)        
        return df

    def retirar_bdrs(self, df):
        df = df[~df['Papel'].str.contains('33')]
        return df

    def retirar_duplicados_mantendo_maior_volume_financeiro(self, df):
        df = df.sort_values("Liq.2meses")
        df = df.drop_duplicates(subset='Papel', keep='last')
        return df

