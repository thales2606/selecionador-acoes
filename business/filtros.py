from pandas._libs.missing import NA


class Filtros:
    def aplicar_filtros(self, df):
        df = self.retirar_seguradoras(df)
        df = self.retirar_bdrs(df)
        df = self.retirar_duplicados_mantendo_maior_volume_financeiro(df)
        df = self.remover_margem_ebit_vazia(df)
        df = self.ordernar_margem_ebit_asc(df)
        return df

    def retirar_seguradoras(self, df):
        df = df[df['Empresa'] != 'SUL AMERICA']
        df = df[df['Empresa'] != 'PORTO SEGURO']
        df = df[df['Empresa'] != 'WIZ S.A.']
        return df

    def retirar_bdrs(self, df):
        df = df[~df['Ação'].str.contains('33')]
        return df

    def retirar_duplicados_mantendo_maior_volume_financeiro(self, df):
        df = df.sort_values("Volume Financ.(R$)")
        df = df.drop_duplicates(subset='Empresa', keep='last')
        return df

    def remover_margem_ebit_vazia(self, df):
        df = df.dropna(subset=['Margem EBIT'])
        return df
    
    def ordernar_margem_ebit_asc(self, df):
        df = df.sort_values("EV/EBIT")
        return df
