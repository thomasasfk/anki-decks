from base import AnkiDeck, DeckMetadata
import genanki
import geopandas as gpd
import matplotlib.pyplot as plt
import requests
from io import BytesIO
import os
import pandas as pd
from typing import Optional
from dataclasses import dataclass


@dataclass
class RegionData:
    name: str
    code: str
    outline_q: bytes
    outline_a: bytes
    flag: Optional[bytes] = None


class WorldRegionsDeck(AnkiDeck):
    def __init__(self, metadata: DeckMetadata):
        super().__init__(metadata)
        self.world = self._load_world_data()
        self.css = self._get_custom_css()

    @staticmethod
    def _load_world_data() -> gpd.GeoDataFrame:
        url = "https://naturalearth.s3.amazonaws.com/110m_cultural/ne_110m_admin_0_countries.zip"
        return gpd.read_file(url)

    def create_model(self) -> genanki.Model:
        return genanki.Model(
            self._model_id,
            'World Regions Model',
            fields=[
                {'name': 'Question'},
                {'name': 'Answer'},
            ],
            templates=[{
                'name': 'Country Card',
                'qfmt': '''
                    <div class="question">
                        {{Question}}
                    </div>
                ''',
                'afmt': '''
                    <div class="answer-container">
                        {{Answer}}
                    </div>
                ''',
            }],
            css=self.css
        )

    def _get_custom_css(self) -> str:
        return """
        .card {
            font-family: Arial, sans-serif;
            background-color: #1a1a1a;
            color: #ffffff;
        }

        .question {
            display: flex;
            justify-content: center;
            padding: 20px;
        }

        .question img {
            max-width: 80%;
            max-height: 80vh;
        }

        .answer-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            padding: 20px;
        }

        .outline-image {
            max-width: 80%;
            max-height: 50vh;
            margin-bottom: 20px;
        }

        .flag-name-container {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 15px;
            margin-top: 10px;
        }

        .            region-flag {
            height: 30px;
            width: auto;
            vertical-align: middle;
        }

        .            region-name {
            font-size: 24px;
            color: #ffffff;
            margin: 0;
            vertical-align: middle;
        }
        """

    def _create_country_image(self, region_name: str, include_neighbors: bool = False, highlighted: bool = False) -> \
    Optional[bytes]:
        country = self.world[self.world.NAME == region_name]
        if country.empty:
            return None

        projected_crs = 'ESRI:54009'
        country_proj = country.to_crs(projected_crs)
        world_proj = self.world.to_crs(projected_crs)

        bounds = country_proj.geometry.total_bounds
        width = bounds[2] - bounds[0]
        height = bounds[3] - bounds[1]
        padding = max(width, height) * 0.2

        fig, ax = plt.subplots(figsize=(10, 10), facecolor='#1a1a1a')
        ax.set_facecolor('#1a1a1a')

        if include_neighbors:
            buffer_distance = max(width, height) * 0.5
            buffered = country_proj.geometry.buffer(buffer_distance)
            neighbors = world_proj[world_proj.geometry.intersects(buffered.iloc[0])]
            neighbors[~neighbors.NAME.eq(region_name)].boundary.plot(
                ax=ax, color='#404040', linewidth=1
            )

        if highlighted:
            country_proj.plot(ax=ax, color='#ff4444', alpha=0.5)
            country_proj.boundary.plot(ax=ax, color='#ffffff', linewidth=2)
        else:
            country_proj.plot(ax=ax, color='#ffffff', alpha=0.9)
            country_proj.boundary.plot(ax=ax, color='#ffffff', linewidth=2)

        ax.set_xlim([bounds[0] - padding, bounds[2] + padding])
        ax.set_ylim([bounds[1] - padding, bounds[3] + padding])
        ax.axis('off')

        img_buffer = BytesIO()
        plt.savefig(
            img_buffer, format='png', bbox_inches='tight', pad_inches=0,
            facecolor='#1a1a1a', edgecolor='none'
        )
        plt.close()
        return img_buffer.getvalue()

    def _get_country_flag(self, region_code: str) -> Optional[bytes]:
        try:
            url = f"https://flagcdn.com/w160/{region_code.lower()}.png"
            response = requests.get(url)
            return response.content
        except:
            return None

    def _get_region_data(self, region_name: str, region_code: str) -> Optional[RegionData]:
        outline_q = self._create_country_image(region_name)
        if outline_q is None:
            return None

        outline_a = self._create_country_image(region_name, include_neighbors=True, highlighted=True)
        flag = self._get_country_flag(region_code)

        return RegionData(
            name=region_name,
            code=region_code,
            outline_q=outline_q,
            outline_a=outline_a,
            flag=flag
        )

    def generate_cards(self) -> list[genanki.Note]:
        notes = []

        for idx, row in self.world.iterrows():
            region_name = row['NAME']
            region_code = row['ISO_A2']

            if pd.isna(region_code) or region_code == '-99':
                continue

            country_data = self._get_region_data(region_name, region_code)
            if country_data is None:
                continue

            # Save media files
            q_filename = f'outline_q_{region_code}.png'
            with open(q_filename, 'wb') as f:
                f.write(country_data.outline_q)
            self.media_files.append(q_filename)

            a_filename = f'outline_a_{region_code}.png'
            with open(a_filename, 'wb') as f:
                f.write(country_data.outline_a)
            self.media_files.append(a_filename)

            flag_html = ''
            if country_data.flag:
                flag_filename = f'flag_{region_code}.png'
                with open(flag_filename, 'wb') as f:
                    f.write(country_data.flag)
                self.media_files.append(flag_filename)
                flag_html = f'<img src="{flag_filename}" class="country-flag">'

            note = genanki.Note(
                model=self.create_model(),
                fields=[
                    f'<img src="{q_filename}">',
                    f'''
                    <img src="{a_filename}" class="outline-image">
                    <div class="flag-name-container">
                        {flag_html}
                        <span class="country-name">{country_data.name}</span>
                    </div>
                    '''
                ]
            )
            notes.append(note)

        return notes


if __name__ == "__main__":
    metadata = DeckMetadata(
        title="World Regions",
        tags=["geography", "territories", "regions", "maps"],
        description="A deck for learning geographic regions and territories on world maps",
        version="1.0.0",
    )

    deck = WorldRegionsDeck(metadata)
    deck.save_deck("world_regions.apkg")

    # Clean up media files
    for file in deck.media_files:
        os.remove(file)