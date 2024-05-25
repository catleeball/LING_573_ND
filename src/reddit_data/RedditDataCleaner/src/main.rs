use std::collections::HashSet;
use std::fs::{File, remove_file};
use std::io;
use std::io::{Lines, BufReader};
// use std::io::BufReader;
// use std::path::Path;
use serde::Serialize;
use serde_json::Value;
use rayon::prelude::*;
use regex::Regex;
use lazy_static::lazy_static;
use std::io::prelude::*;
use anyhow::{anyhow, Result};
// use zstd::stream::read::Decoder;
use std::process::Command;

// lol, lmao,
lazy_static!{
    static ref PATHS: [String; 440] = [
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2023-05.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2013-09.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2008-12.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2015-02.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2019-06.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2016-02.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2013-10.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2017-03.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2019-07.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2021-06.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2017-01.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2017-06.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2006-10.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2020-06.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2007-09.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2012-09.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2014-02.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2010-04.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2012-06.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2018-07.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2015-09.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2019-01.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2022-10.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2008-05.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2021-12.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2018-05.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2008-04.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2007-11.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2008-02.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2021-07.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2008-03.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2011-07.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2013-01.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2023-01.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2007-10.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2013-02.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2012-01.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2008-09.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2006-09.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2016-06.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2006-11.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2009-09.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2013-07.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2015-11.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2014-03.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2010-01.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2021-05.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2010-05.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2017-02.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2023-07.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2012-02.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2013-04.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2011-09.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2008-06.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2020-05.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2006-05.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2020-12.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2023-08.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2006-04.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2007-06.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2010-09.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2010-02.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2012-08.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2016-04.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2016-12.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2020-09.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2018-03.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2018-08.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2016-08.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2015-05.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2017-10.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2021-10.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2020-11.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2023-03.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2019-11.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2016-03.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2009-03.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2017-11.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2008-01.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2017-07.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2015-03.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2007-12.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2012-10.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2010-07.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2011-12.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2008-11.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2015-06.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2020-01.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2007-05.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2022-02.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2020-07.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2007-07.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2009-06.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2014-09.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2021-04.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2015-04.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2008-07.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2021-02.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2022-08.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2022-12.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2020-02.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2023-09.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2018-06.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2013-12.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2021-08.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2023-06.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2018-12.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2009-02.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2021-01.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2009-04.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2017-04.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2008-08.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2019-02.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2005-12.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2023-10.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2010-03.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2009-12.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2014-11.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2018-02.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2012-12.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2010-06.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2017-05.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2010-10.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2019-05.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2019-12.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2009-08.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2007-02.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2018-10.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2023-12.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2007-08.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2018-09.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2016-05.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2006-12.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2012-04.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2013-11.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2007-04.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2009-01.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2006-06.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2010-11.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2014-12.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2015-07.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2022-05.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2018-01.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2009-07.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2023-02.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2011-01.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2022-06.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2014-04.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2022-11.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2020-04.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2012-05.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2017-12.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2007-01.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2007-03.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2022-03.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2020-10.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2018-04.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2016-10.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2006-03.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2012-03.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2014-07.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2016-07.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2018-11.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2014-10.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2009-05.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2012-11.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2022-07.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2015-08.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2015-01.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2016-11.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2021-03.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2011-08.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2022-01.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2019-08.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2014-01.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2014-08.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2006-07.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2020-03.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2014-06.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2011-04.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2006-08.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2011-02.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2009-11.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2016-09.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2008-10.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2013-08.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2021-09.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2015-12.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2016-01.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2017-08.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2011-05.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2017-09.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2014-05.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2015-10.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2011-11.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2011-03.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2013-05.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2023-04.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2021-11.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2009-10.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2019-04.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2023-11.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2020-08.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2010-08.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2006-02.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2011-06.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2013-03.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2006-01.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2011-10.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2019-03.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2022-09.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2019-10.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2013-06.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2022-04.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2010-12.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2012-07.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/comments/RC_2019-09.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2022-07.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2011-07.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2008-03.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2018-07.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2021-09.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2021-10.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2013-12.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2016-03.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2017-07.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2007-09.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2017-12.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2023-01.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2008-10.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2009-10.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2018-09.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2008-06.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2012-02.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2023-09.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2011-12.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2023-12.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2014-05.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2017-01.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2018-05.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2015-03.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2018-03.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2015-12.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2010-01.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2023-04.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2012-11.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2013-10.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2011-01.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2018-08.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2014-07.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2008-01.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2015-09.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2007-12.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2007-04.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2015-08.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2021-12.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2016-01.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2006-07.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2006-03.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2023-08.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2005-12.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2007-06.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2014-04.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2007-02.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2008-12.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2016-10.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2022-06.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2006-12.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2005-08.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2016-09.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2016-07.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2013-08.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2017-11.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2019-02.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2019-11.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2018-06.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2019-12.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2021-11.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2007-01.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2019-10.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2005-06.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2010-09.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2011-04.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2006-10.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2015-10.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2005-09.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2016-06.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2016-08.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2014-12.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2015-07.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2019-08.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2012-05.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2019-05.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2023-02.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2023-03.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2006-08.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2014-01.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2013-11.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2006-09.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2023-05.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2017-02.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2019-09.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2008-04.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2021-02.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2022-05.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2019-03.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2020-04.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2023-10.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2020-06.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2016-11.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2006-11.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2021-05.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2021-04.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2007-10.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2016-05.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2018-11.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2015-04.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2020-09.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2006-01.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2022-08.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2008-11.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2022-03.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2013-03.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2009-12.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2010-12.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2017-03.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2019-04.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2015-01.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2022-04.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2023-07.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2009-02.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2021-08.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2016-04.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2009-04.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2019-01.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2015-05.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2017-10.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2008-08.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2020-07.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2017-04.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2006-04.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2006-02.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2013-09.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2021-03.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2022-11.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2010-06.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2009-09.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2011-11.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2012-09.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2010-05.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2008-09.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2012-12.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2021-01.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2014-10.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2022-12.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2015-11.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2017-05.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2009-05.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2011-10.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2012-01.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2016-12.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2011-03.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2023-11.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2021-07.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2020-11.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2010-08.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2019-07.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2013-02.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2007-08.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2015-02.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2022-09.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2022-02.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2018-02.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2005-07.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2018-04.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2023-06.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2009-08.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2017-06.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2020-02.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2007-05.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2020-05.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2007-03.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2014-02.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2014-11.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2020-03.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2009-06.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2020-10.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2012-08.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2012-06.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2021-06.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2005-10.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2012-03.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2010-11.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2011-05.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2006-06.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2009-03.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2011-08.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2013-07.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2018-10.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2020-08.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2012-04.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2008-07.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2017-08.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2006-05.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2009-11.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2016-02.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2012-10.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2015-06.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2011-09.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2014-03.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2014-09.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2022-10.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2014-08.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2008-05.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2018-12.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2020-12.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2010-04.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2007-11.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2020-01.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2009-07.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2010-02.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2013-06.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2017-09.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2010-07.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2008-02.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2013-05.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2010-10.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2010-03.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2007-07.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2018-01.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2014-06.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2005-11.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2022-01.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2013-01.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2011-06.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2011-02.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2012-07.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2009-01.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2013-04.zst"),
        String::from("/Media/Data/reddit/Full_Reddit_Data/submissions/RS_2019-06.zst"),
    ];
    static ref EXTRA_ALLOWED_CHARS: HashSet<char> = HashSet::from([' ', '?', '!', '/']);
    static ref SARCASTIC_REGEX: Regex = Regex::new(r###"(?:[^\s]?[/\\]s[\S$.,?!]?|[^\s]?[/\\]sarcasm[\s$.,?!]?|[^\s]?[/\\]sarcastic[\s$.,?!]?)"###).expect("Failed to compile regex");
    static ref SERIOUS_REGEX: Regex = Regex::new(r###"(?:[^\s]?[/\\]serious[\s$.,?!]?|[^\s]?[/\\]srs[\s$.,?!]?)"###).expect("Failed to compile regex");
    static ref URL_REGEX: Regex = Regex::new(r###"['"(]*http[\S)'"$]+"###).expect("Failed to compile regex");
}

/// A single Comment or Submission from Reddit
///
/// Documentation on Comment and Submission models:
///   - https://praw.readthedocs.io/en/stable/code_overview/models/comment.html
///   - https://praw.readthedocs.io/en/stable/code_overview/models/submission.html
#[derive(Serialize, Debug)]
struct RedditPost {
    id:           String,
    text:         String,  // From `body` or `selftext`
    author:       String,
    title:        String,  // Only submissions have these
    subreddit:    String,
    subreddit_id: String,
    permalink:    String,
    created_utc:  u32,     // we shouldn't have any posts before 1970 or in the future
    sarcastic:    bool,
    serious:      bool,
}
/// Deserialize JSONL data into a RedditPost struct.
impl RedditPost {
    fn from_jsonl(json_line: &str) -> Result<RedditPost> {
        let json_post: Value = serde_json::from_str(json_line)?;

        let mut text: String;
        if json_post["body"] != Value::Null {
            text = json_post["body"].to_string();
        } else if json_post["selftext"] != Value::Null {
            text = json_post["selftext"].to_string();
        } else {
            println!("Json line has no attribute `selftext` or `body`. Got line: {json_line}");
            return Err(anyhow!("Json line has no attribute `selftext` or `body`. Got line: {json_line}"))
        }

        let mut title: String = String::from("");
        if json_post["title"] != Value::Null {
            title = json_post["title"].to_string();
        }

        let id = json_post["id"].to_string()
            .par_chars()
            .filter(|c| c.is_ascii_alphanumeric() || c.is_ascii_digit() || EXTRA_ALLOWED_CHARS.contains(c))
            .collect::<String>();
        text = text
            .par_chars()
            .filter(|c| c.is_ascii_alphanumeric() || c.is_ascii_digit() || EXTRA_ALLOWED_CHARS.contains(c))
            .collect::<String>();
        title = title
            .par_chars()
            .filter(|c| c.is_ascii_alphanumeric() || c.is_ascii_digit() || EXTRA_ALLOWED_CHARS.contains(c))
            .collect::<String>();
        let author = json_post["author"].to_string()
            .par_chars()
            .filter(|c| c.is_ascii_alphanumeric() || c.is_ascii_digit() || EXTRA_ALLOWED_CHARS.contains(c))
            .collect::<String>();
        let subreddit = json_post["subreddit"].to_string()
            .par_chars()
            .filter(|c| c.is_ascii_alphanumeric() || c.is_ascii_digit() || EXTRA_ALLOWED_CHARS.contains(c))
            .collect::<String>();
        let subreddit_id = json_post["subreddit_id"].to_string()
            .par_chars()
            .filter(|c| c.is_ascii_alphanumeric() || c.is_ascii_digit() || EXTRA_ALLOWED_CHARS.contains(c))
            .collect::<String>();
        let permalink = json_post["permalink"].to_string()
            .par_chars()
            .filter(|c| c.is_ascii_alphanumeric() || c.is_ascii_digit() || EXTRA_ALLOWED_CHARS.contains(c))
            .collect::<String>();
        let created_utc = json_post["created_utc"].to_string()
            .par_chars()
            .filter(|c| c.is_ascii_alphanumeric() || c.is_ascii_digit() || EXTRA_ALLOWED_CHARS.contains(c))
            .collect::<String>();

        Ok(RedditPost{
            id,
            author,
            text: text.clone(),
            title,
            subreddit,
            subreddit_id,
            permalink,
            created_utc: created_utc.parse::<u32>().unwrap_or(0),
            sarcastic: SARCASTIC_REGEX.is_match(&text),
            serious: SERIOUS_REGEX.is_match(&text),
        })
    }
}

// #[inline]
// fn read_lines<P>(filename: P) -> io::Result<io::Lines<BufReader<File>>>
//     where P: AsRef<Path>, {
//     let file = File::open(filename)?;
//     Ok(BufReader::new(file).lines())
// }

#[inline]
fn read_lines(filename: &str) -> Lines<BufReader<File>> {
    let file = File::open(filename).expect(&format!("Failed to open file {filename}"));
    BufReader::new(file).lines()
}

// #[inline]
// fn read_lines<P>(filename: P) -> Result<String>
//     where
//         P: AsRef<Path>,
// {
//     let file = File::open(filename)?;
//     let mut decoder = Decoder::new(file)?;
//     decoder.window_log_max(31)?;
//     let mut str_buffer = String::new();
//     BufReader::new(decoder).read_to_string(&mut str_buffer)?;
//     Ok(str_buffer)
// }

#[inline]
fn decompress_file(filename: &str) -> String {
    let output = Command::new("zstd")
        .args(["--decompress", "-T0", "--long=31", filename])
        .output()
        .expect(&format!("Failed to decompress {filename}"));
    io::stdout().write_all(&output.stdout).unwrap();
    io::stderr().write_all(&output.stderr).unwrap();
    let decomp = filename.replace(".zst", "");
    decomp
}

/// Given a data file, decompress it if needed, process all the json lines as RedditPosts, then
/// write them into a new file.
#[inline]
fn clean_file(filename: &str) -> Vec<String> {
    read_lines(filename)
        .filter_map(|line| line.ok())
            .filter(|line| {
                let result = line.starts_with('{') && line.ends_with('}');
                if result == false {
                    println!("Bad line: {line}");
                }
                result
            })
            .map(|line| line.par_chars()
                .filter(|c| c.is_ascii())
                .collect::<String>()
            )
            .map(|line| line.replace("\n", " "))
            .map(|line| line.replace("\\", "/"))
            .map(|line| { RedditPost::from_jsonl(&line) })
            .filter_map(|post| post.ok())
            .map(|post| serde_json::to_string(&post))
            .filter_map(|line| line.ok())
            .collect()
}

fn main() {
    for path in PATHS.iter() {
        // let filehandle = match File::open(&path) {
        //     Ok(fh) => fh,
        //     Err(e) => {
        //         println!("[WARN] Failed to open file: `{path}`. Error: {e}");
        //         continue
        //     },
        // };
        // let bufreader = BufReader::new(filehandle);
        // let mut zstd_reader = match Decoder::with_buffer(bufreader) {
        //     Ok(dec) => dec,
        //     Err(e) => {
        //         println!("[WARN] Failed to decompress: `{path}`. Error: {e}");
        //         continue
        //     }
        // };
        // match zstd_reader.window_log_max(31) {
        //     Ok(dec) => dec,
        //     Err(e) => {
        //         println!("[WARN] Failed to set windlow_log_max for file: `{path}`. Error: {e}");
        //         continue
        //     }
        // };

        let decompressed = decompress_file(&path);
        println!("Decompressed file: {decompressed}");

        let cleaned_json = clean_file(&decompressed).join("\n");

        println!("{} lines parsed from {}", &cleaned_json.len(), &path);

        let new_file_path = format!("{}{}", path, ".PROCESSED.jsonl");
        let mut file = match File::create(new_file_path) {
            Ok(file) => file,
            Err(e) => {
                println!("[ERR] Failed to open new file. Error: {e}");
                continue
            },
        };
        match file.write_all(cleaned_json.as_bytes()) {
            Ok(_) => (),
            Err(e) => {
                println!("[ERR] Failed to write bytes. Error: {e}");
                continue
            },
        };
        match remove_file(&decompressed) {
            Ok(_) => (),
            Err(e) => {
                println!("[ERR] Failed to delete file {}. Error: {}", &decompressed, e);
                continue
            }
        };
    }
}
