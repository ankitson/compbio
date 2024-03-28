use std::fs::File;

use anyhow::Result;
use chrono::prelude::*;
use polars::prelude::*;
fn main() -> Result<()> {
    println!("Hello, world!");

    let mut df: DataFrame = df!(
        "integer" => &[1, 2, 3],
        "date" => &[
                NaiveDate::from_ymd_opt(2022, 1, 1).unwrap().and_hms_opt(0, 0, 0).unwrap(),
                NaiveDate::from_ymd_opt(2022, 1, 2).unwrap().and_hms_opt(0, 0, 0).unwrap(),
                NaiveDate::from_ymd_opt(2022, 1, 3).unwrap().and_hms_opt(0, 0, 0).unwrap(),
        ],
        "float" => &[4.0, 5.0, 6.0]
    )
    .unwrap();
    println!("{}", df);

    let mut file = File::create("output.csv").expect("could not create file");
    CsvWriter::new(&mut file)
        .include_header(true)
        .with_separator(b',')
        .finish(&mut df)?;
    let df_csv = CsvReader::from_path("output.csv")?
        .infer_schema(None)
        .has_header(true)
        .with_try_parse_dates(true)
        .finish()?;
    println!("{}", df_csv);
    Ok(())
}
