from sqlmodel import SQLModel,Field,create_engine

#all the compositions of Salvador Martínez García
class composition(SQLModel, table = True):
    title: str = Field(default = None, primary_key = True)
    alternate_title: str | None = None
    internal_ref_number: str | None = None
    key: str | None = None
    composition_year: int | None = None
    first_performance_year: int | None = None
    avg_duration: int | None = None
    composer_time_period: str | None = None
    piece_style: str | None = None
    instrumentation: str | None = None

#the sheet music scans available for each composition
class scans(SQLModel, table = True):
    piece_title: str = Field(default = None, foreign_key = "composition.title")
    scan_type: str | None = None
    scan_id: int = Field(default = None, primary_key = True)
    page_count: int | None = None

engine = create_engine('sqlite:///SMG_Pieces.db')
SQLModel.metadata.create_all(engine)