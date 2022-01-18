from pandas._libs.missing import NA


class Filtros:
    def aplicar_filtros(self, df):
        df = self.retirar_seguradoras(df)
        df = self.retirar_bdrs(df)
        df = self.retirar_duplicados_mantendo_maior_volume_financeiro(df)
        df = self.remover_margem_ebit_vazia(df)
        df = self.ordernar_ev_ebit_asc(df)
        df = self.ranquear_por_ev_ebit_asc(df)
        df = self.ordernar_roic_desc(df)
        df = self.ranquear_por_roic_desc(df)
        df = self.gerar_rank_geral(df)
        df = self.ordernar_rank_geral_asc(df)
        return df

    def retirar_seguradoras(self, df):
        df = df[df['Empresa'] != 'SUL AMERICA']
        df = df[df['Empresa'] != 'PORTO SEGURO']
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

    def ordernar_ev_ebit_asc(self, df):
        df = df.sort_values("EV/EBIT")
        return df

    def ranquear_por_ev_ebit_asc(self, df):
        df['Rank EV/EBIT'] = df[['EV/EBIT', 'Ação']].apply(tuple, axis=1)\
            .rank(method='dense', ascending=True).astype(int)
        return df

    def ordernar_roic_desc(self, df):
        df['ROInvC'] = df['ROInvC'].str.replace(',','.').str.rstrip('%').astype('float') / 100.0
        df = df.sort_values("ROInvC", ascending=False)
        return df

    def ranquear_por_roic_desc(self, df):
        df['Rank ROInvC'] = df[['ROInvC', 'Ação']].apply(tuple, axis=1)\
            .rank(method='dense', ascending=False).astype(int)
        return df

    def gerar_rank_geral(self, df):
        sum_column = df["Rank EV/EBIT"] + df["Rank ROInvC"]
        df['Rank Geral'] = sum_column
        return df

    def ordernar_rank_geral_asc(self, df):
        df = df.sort_values("Rank Geral", ascending=True)
        return df
