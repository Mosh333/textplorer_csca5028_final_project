// render_data.js

function processSingleInputDataTextInput(analysisResult) {
    const topNWordsData = analysisResult.basic_text_analysis_dict.top_n_words;
    const words = topNWordsData.map(item => item[0]);
    const frequencies = topNWordsData.map(item => item[1]);

    // Show the analysis result elements
    document.getElementById('analysis-results-text-input').style.display = 'block';
    document.getElementById('loading-message-text-input').remove();

    // Basic Text Analysis
    const basicTextAnalysisDict = analysisResult.basic_text_analysis_dict;
    const basicTextAnalysisContainer = document.getElementById('basic-text-analysis-container-text-input');
    basicTextAnalysisContainer.innerHTML = ''; // Clear previous content

    const basicTextAnalysisTable = document.createElement('table');
    for (const [key, value] of Object.entries(basicTextAnalysisDict)) {
        const row = document.createElement('tr');
        const keyCell = document.createElement('td');
        keyCell.textContent = key;
        const valueCell = document.createElement('td');
        if (key === 'estimated_reading_time') {
            valueCell.textContent = `${value} min(s)`;
        } else {
            valueCell.textContent = value;
        }
        row.appendChild(keyCell);
        row.appendChild(valueCell);
        basicTextAnalysisTable.appendChild(row);
    }
    basicTextAnalysisContainer.appendChild(basicTextAnalysisTable);

    // Sentiment Analysis
    const sentimentAnalysisDict = analysisResult.sentiment_analysis_dict;
    const sentimentAnalysisContainer = document.getElementById('sentiment-analysis-container-text-input');
    sentimentAnalysisContainer.innerHTML = ''; // Clear previous content

    const sentimentAnalysisTable = document.createElement('table');
    for (const [key, value] of Object.entries(sentimentAnalysisDict)) {
        const row = document.createElement('tr');
        const keyCell = document.createElement('td');
        keyCell.textContent = key;
        const valueCell = document.createElement('td');
        valueCell.textContent = value;
        row.appendChild(keyCell);
        row.appendChild(valueCell);
        sentimentAnalysisTable.appendChild(row);
    }
    sentimentAnalysisContainer.appendChild(sentimentAnalysisTable);

    // NLP Analysis
    const nlpAnalysisDict = analysisResult.nlp_analysis_dict;
    const nlpAnalysisContainer = document.getElementById('nlp-analysis-container-text-input');
    nlpAnalysisContainer.innerHTML = ''; // Clear previous content

    const nlpAnalysisTable = document.createElement('table');
    for (const [key, value] of Object.entries(nlpAnalysisDict)) {
        const row = document.createElement('tr');
        const keyCell = document.createElement('td');
        keyCell.textContent = key;
        const valueCell = document.createElement('td');
        if (typeof value === 'object') {
            valueCell.textContent = JSON.stringify(value);
        } else {
            valueCell.textContent = value;
        }
        row.appendChild(keyCell);
        row.appendChild(valueCell);
        nlpAnalysisTable.appendChild(row);
    }
    nlpAnalysisContainer.appendChild(nlpAnalysisTable);

    // Bar Graphs
    var ctxWord = document.getElementById('myChart-text-input').getContext('2d');
    var wordChart = new Chart(ctxWord, {
        type: 'bar',
        data: {
            labels: words,
            datasets: [{
                label: 'Word Frequency',
                data: frequencies,
                backgroundColor: 'rgba(75, 192, 192, 0.2)', // Light green
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });

    const posCountData = analysisResult.nlp_analysis_dict.pos_count;
    const posTagNames = {
        'NN': 'Noun',
        'DT': 'Determiner',
        'NNP': 'Proper Noun',
        'IN': 'Preposition or Subordinating Conjunction',
        'NNS': 'Plural Noun',
        'JJ': 'Adjective',
        ',': 'Comma',
        'PRP': 'Personal Pronoun',
        'RB': 'Adverb',
        'VB': 'Verb (base form)',
        'VBD': 'Verb (past tense)',
        'TO': 'to',
        'VBP': 'Verb (non-3rd person singular present)',
        '.': 'Period',
        'VBG': 'Verb (gerund or present participle)',
        'VBZ': 'Verb (3rd person singular present)',
        'CC': 'Coordinating Conjunction',
        "''": 'Closing quotation mark',
        '``': 'Opening quotation mark',
        'PRP$': 'Possessive Pronoun',
        'CD': 'Cardinal Number',
        'VBN': 'Verb (past participle)',
        'WDT': 'Wh-Determiner',
        'MD': 'Modal',
        'RP': 'Particle',
        '$': 'Dollar Sign',
        'WRB': 'Wh-Adverb',
        'POS': 'Possessive Ending',
        'WP': 'Wh-Pronoun',
        'JJS': 'Adjective (superlative)',
        ':': 'Colon',
        'JJR': 'Adjective (comparative)',
        'RBR': 'Adverb (comparative)'
    };

    const top5PosCount = Object.entries(posCountData)
        .sort((a, b) => b[1] - a[1])
        .slice(0, 5);

    const posLabels = top5PosCount.map(item => posTagNames[item[0]]);
    const posCounts = top5PosCount.map(item => item[1]);

    var ctxPos = document.getElementById('posChart-text-input').getContext('2d');
    var posChart = new Chart(ctxPos, {
        type: 'bar',
        data: {
            labels: posLabels,
            datasets: [{
                label: 'POS Tag Count',
                data: posCounts,
                backgroundColor: 'rgba(75, 192, 192, 0.2)', // Light green
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}

function processSingleInputDataNewsArticle(analysisResult) {
    const topNWordsData = analysisResult.basic_text_analysis_dict.top_n_words;
    const words = topNWordsData.map(item => item[0]);
    const frequencies = topNWordsData.map(item => item[1]);

    // Show the analysis result elements
    document.getElementById('analysis-results-news-article').style.display = 'block';
    document.getElementById('loading-message-news-article').remove();
    var linkNewsArticle = document.getElementById('link-news-article');
    var textDataNewsArticle = document.getElementById('text-data-news-article');

    // Update the above contents
    linkNewsArticle.innerHTML = 'Selected News Article Link: <a href="' + analysisResult.article_link + '">' + analysisResult.article_link + '</a>';
    textDataNewsArticle.textContent = analysisResult.article_text_data;

    // Display elements:
    linkNewsArticle.style.display = 'block';
    textDataNewsArticle.style.display = 'block';

    // Basic Text Analysis
    const basicTextAnalysisDict = analysisResult.basic_text_analysis_dict;
    const basicTextAnalysisContainer = document.getElementById('basic-text-analysis-container-news-article');
    basicTextAnalysisContainer.innerHTML = ''; // Clear previous content

    const basicTextAnalysisTable = document.createElement('table');
    for (const [key, value] of Object.entries(basicTextAnalysisDict)) {
        const row = document.createElement('tr');
        const keyCell = document.createElement('td');
        keyCell.textContent = key;
        const valueCell = document.createElement('td');
        if (key === 'estimated_reading_time') {
            valueCell.textContent = `${value} min(s)`;
        } else {
            valueCell.textContent = value;
        }
        row.appendChild(keyCell);
        row.appendChild(valueCell);
        basicTextAnalysisTable.appendChild(row);
    }
    basicTextAnalysisContainer.appendChild(basicTextAnalysisTable);

    // Sentiment Analysis
    const sentimentAnalysisDict = analysisResult.sentiment_analysis_dict;
    const sentimentAnalysisContainer = document.getElementById('sentiment-analysis-container-news-article');
    sentimentAnalysisContainer.innerHTML = ''; // Clear previous content

    const sentimentAnalysisTable = document.createElement('table');
    for (const [key, value] of Object.entries(sentimentAnalysisDict)) {
        const row = document.createElement('tr');
        const keyCell = document.createElement('td');
        keyCell.textContent = key;
        const valueCell = document.createElement('td');
        valueCell.textContent = value;
        row.appendChild(keyCell);
        row.appendChild(valueCell);
        sentimentAnalysisTable.appendChild(row);
    }
    sentimentAnalysisContainer.appendChild(sentimentAnalysisTable);

    // NLP Analysis
    const nlpAnalysisDict = analysisResult.nlp_analysis_dict;
    const nlpAnalysisContainer = document.getElementById('nlp-analysis-container-news-article');
    nlpAnalysisContainer.innerHTML = ''; // Clear previous content

    const nlpAnalysisTable = document.createElement('table');
    for (const [key, value] of Object.entries(nlpAnalysisDict)) {
        const row = document.createElement('tr');
        const keyCell = document.createElement('td');
        keyCell.textContent = key;
        const valueCell = document.createElement('td');
        if (typeof value === 'object') {
            valueCell.textContent = JSON.stringify(value);
        } else {
            valueCell.textContent = value;
        }
        row.appendChild(keyCell);
        row.appendChild(valueCell);
        nlpAnalysisTable.appendChild(row);
    }
    nlpAnalysisContainer.appendChild(nlpAnalysisTable);

    // Bar Graphs
    var ctxWord = document.getElementById('myChart-news-article').getContext('2d');
    var wordChart = new Chart(ctxWord, {
        type: 'bar',
        data: {
            labels: words,
            datasets: [{
                label: 'Word Frequency',
                data: frequencies,
                backgroundColor: 'rgba(75, 192, 192, 0.2)', // Light green
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });

    const posCountData = analysisResult.nlp_analysis_dict.pos_count;
    const posTagNames = {
        'NN': 'Noun',
        'DT': 'Determiner',
        'NNP': 'Proper Noun',
        'IN': 'Preposition or Subordinating Conjunction',
        'NNS': 'Plural Noun',
        'JJ': 'Adjective',
        ',': 'Comma',
        'PRP': 'Personal Pronoun',
        'RB': 'Adverb',
        'VB': 'Verb (base form)',
        'VBD': 'Verb (past tense)',
        'TO': 'to',
        'VBP': 'Verb (non-3rd person singular present)',
        '.': 'Period',
        'VBG': 'Verb (gerund or present participle)',
        'VBZ': 'Verb (3rd person singular present)',
        'CC': 'Coordinating Conjunction',
        "''": 'Closing quotation mark',
        '``': 'Opening quotation mark',
        'PRP$': 'Possessive Pronoun',
        'CD': 'Cardinal Number',
        'VBN': 'Verb (past participle)',
        'WDT': 'Wh-Determiner',
        'MD': 'Modal',
        'RP': 'Particle',
        '$': 'Dollar Sign',
        'WRB': 'Wh-Adverb',
        'POS': 'Possessive Ending',
        'WP': 'Wh-Pronoun',
        'JJS': 'Adjective (superlative)',
        ':': 'Colon',
        'JJR': 'Adjective (comparative)',
        'RBR': 'Adverb (comparative)'
    };

    const top5PosCount = Object.entries(posCountData)
        .sort((a, b) => b[1] - a[1])
        .slice(0, 5);

    const posLabels = top5PosCount.map(item => posTagNames[item[0]]);
    const posCounts = top5PosCount.map(item => item[1]);

    var ctxPos = document.getElementById('posChart-news-article').getContext('2d');
    var posChart = new Chart(ctxPos, {
        type: 'bar',
        data: {
            labels: posLabels,
            datasets: [{
                label: 'POS Tag Count',
                data: posCounts,
                backgroundColor: 'rgba(75, 192, 192, 0.2)', // Light green
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}

// analysis_results, file_info, loop_index
function processFilesInputData(analysisResults) {
    if (Object.keys(analysisResults).length > 1) {
        var loadingMessage = document.getElementById("loading-message-files-input");

        // display property to "none" to hide it
        loadingMessage.style.display = "none";
    }
    console.log("analysisResults is: ", analysisResults);
    var container = document.getElementById("files_input-container");

    // Create a copy of analysisResults without the "request_id" key
    var newAnalysisResults = Object.assign({}, analysisResults);
    delete newAnalysisResults['request_id'];

    // Iterate over the keys of newAnalysisResults
    var keys = Object.keys(newAnalysisResults);
    for (var i = 0; i < keys.length; i++) {
        var key = keys[i];
        var fileInfo = newAnalysisResults[key];

        // Create a new div element
        var div = document.createElement('div');
        div.id = 'files_input-analysis-' + i;

        // Add Provided Text Input Data
        var providedTextInputDataDiv = document.createElement('div');
        providedTextInputDataDiv.innerHTML = '<h2>Provided Text Input Data:</h2>' +
            '<p>Filename: ' + key + '</p>' +
            '<p>File Size: ' + fileInfo.file_size + ' bytes' + '</p>' +
            '<p>Text Content: ' + fileInfo.text_content + '</p>';
        div.appendChild(providedTextInputDataDiv);

        console.log(fileInfo)
        console.log(fileInfo.analysis_result)
        // add basic text analysis chart title
        var titleElement = document.createElement('h4');
        titleElement.innerHTML = 'Top 5 Common Words';
        titleElement.style.textAlign = 'center';
        div.appendChild(titleElement);
        // Add Basic Text Analysis Chart
        var wordChartDiv = document.createElement('div');
        wordChartDiv.innerHTML = '<canvas id="wordChart_' + i + '" width="400" height="200"></canvas>';
        div.appendChild(wordChartDiv);


        // Add Basic Text Analysis
        var basicTextAnalysisDiv = document.createElement('div');
        basicTextAnalysisDiv.innerHTML = '<h2>Basic Text Analysis:</h2>' +
            '<div id="basic-text-analysis-container-' + i + '">' +
            '<table>' +
            '<tr><td>average_sentences_size</td><td>' + fileInfo.analysis_result.basic_text_analysis_dict.average_sentences_size + '</td></tr>' +
            '<tr><td>average_word_size</td><td>' + fileInfo.analysis_result.basic_text_analysis_dict.average_word_size + '</td></tr>' +
            '<tr><td>difficulty_level</td><td>' + fileInfo.analysis_result.basic_text_analysis_dict.difficulty_level + '</td></tr>' +
            '<tr><td>estimated_reading_time</td><td>' + fileInfo.analysis_result.basic_text_analysis_dict.estimated_reading_time + ' min(s)' + '</td></tr>' +
            '<tr><td>num_characters_without_spaces</td><td>' + fileInfo.analysis_result.basic_text_analysis_dict.num_characters_without_spaces + '</td></tr>' +
            '<tr><td>num_paragraphs</td><td>' + fileInfo.analysis_result.basic_text_analysis_dict.num_paragraphs + '</td></tr>' +
            '<tr><td>num_sentences</td><td>' + fileInfo.analysis_result.basic_text_analysis_dict.num_sentences + '</td></tr>' +
            '<tr><td>num_syllables</td><td>' + fileInfo.analysis_result.basic_text_analysis_dict.num_syllables + '</td></tr>' +
            '<tr><td>top_n_words</td><td>' + fileInfo.analysis_result.basic_text_analysis_dict.top_n_words + '</td></tr>' +
            '<tr><td>word_count</td><td>' + fileInfo.analysis_result.basic_text_analysis_dict.word_count + '</td></tr>' +
            '</table>' +
            '</div>';
        div.appendChild(basicTextAnalysisDiv);

        // Add Sentiment Analysis
        var sentimentAnalysisDiv = document.createElement('div');
        sentimentAnalysisDiv.innerHTML = '<h2>Sentiment Analysis:</h2>' +
            '<div id="sentiment-analysis-container-' + i + '">' +
            '<table>' +
            '<tr><td>domain_category</td><td>' + fileInfo.analysis_result.sentiment_analysis_dict.domain_category + '</td></tr>' +
            '<tr><td>emotion</td><td>' + fileInfo.analysis_result.sentiment_analysis_dict.emotion + '</td></tr>' +
            '<tr><td>sentiment</td><td>' + fileInfo.analysis_result.sentiment_analysis_dict.sentiment + '</td></tr>' +
            '</table>' +
            '</div>';
        sentimentAnalysisDiv.innerHTML += '</table></div>';
        div.appendChild(sentimentAnalysisDiv);


        // add pos tag chart title
        var posTitleElement = document.createElement('h4');
        posTitleElement.innerHTML = 'POS Tag Analysis';
        posTitleElement.style.textAlign = 'center';
        div.appendChild(posTitleElement);

        // add pos tag chart
        var posChartDiv = document.createElement('div');
        posChartDiv.innerHTML = '<canvas id="posChart_' + i + '" width="400" height="200"></canvas>';
        div.appendChild(posChartDiv);
        // Add NLP Analysis
        var nlpAnalysisDiv = document.createElement('div');
        nlpAnalysisDiv.innerHTML = '<h2>NLP Analysis:</h2>' +
            '<div id="nlp-analysis-container-' + i + '">' +
            '<table>' +
            '<tr><td>ner</td><td>' + fileInfo.analysis_result.nlp_analysis_dict.ner + '</td></tr>' +
            '<tr><td>pos_count</td><td>' + JSON.stringify(fileInfo.analysis_result.nlp_analysis_dict.pos_count) + '</td></tr>' +
            '</table></div>'; // divider line

        div.appendChild(nlpAnalysisDiv);

        // Add links container
        var linksContainerDiv = document.createElement('div');
        linksContainerDiv.className = 'links-container';
        linksContainerDiv.innerHTML = '<p>For more information on POS tags, you can visit:</p>' +
            '<ul>' +
            '<li><a href="https://stackoverflow.com/questions/15388831/what-are-all-possible-pos-tags-of-nltk" target="_blank">Stack Overflow - Possible POS tags of NLTK</a></li>' +
            '<li><a href="https://www.ling.upenn.edu/courses/Fall_2003/ling001/penn_treebank_pos.html" target="_blank">Penn Treebank POS Tags</a></li>' +
            '</ul>';
        div.appendChild(linksContainerDiv);

        var hrElement = document.createElement('hr');
        div.appendChild(hrElement);

        // Append the div to the container
        container.appendChild(div);


        // Draw the basic text analysis bar graph
        // get data for the chart
        const top5WordsData = fileInfo.analysis_result.basic_text_analysis_dict.top_n_words;
        // get words and frequencies
        const words = top5WordsData.map(item => item[0]);
        const frequencies = top5WordsData.map(item => item[1]);
        // instantiate a new Chart instance for top 5 words
        var ctx_word = document.getElementById('wordChart_' + i).getContext('2d');
        var wordChart = new Chart(ctx_word, {
            type: 'bar',
            data: {
                labels: words,
                datasets: [{
                    label: 'Word Frequency',
                    data: frequencies,
                    backgroundColor: 'rgba(75, 192, 192, 0.2)', // Light green
                    borderColor: 'rgba(75, 192, 192, 1)',
                    borderWidth: 1
                }]
            },
            options: {
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
        // Finished the basic text analysis bar graph
        // Draw the pos tag chart
        const posCountData = fileInfo.analysis_result.nlp_analysis_dict.pos_count;

        // pos map
        const posTagNames = {
            'NN': 'Noun',
            'DT': 'Determiner',
            'NNP': 'Proper Noun',
            'IN': 'Preposition or Subordinating Conjunction',
            'NNS': 'Plural Noun',
            'JJ': 'Adjective',
            ',': 'Comma',
            'PRP': 'Personal Pronoun',
            'RB': 'Adverb',
            'VB': 'Verb (base form)',
            'VBD': 'Verb (past tense)',
            'TO': 'to',
            'VBP': 'Verb (non-3rd person singular present)',
            '.': 'Period',
            'VBG': 'Verb (gerund or present participle)',
            'VBZ': 'Verb (3rd person singular present)',
            'CC': 'Coordinating Conjunction',
            "''": 'Closing quotation mark',
            '``': 'Opening quotation mark',
            'PRP$': 'Possessive Pronoun',
            'CD': 'Cardinal Number',
            'VBN': 'Verb (past participle)',
            'WDT': 'Wh-Determiner',
            'MD': 'Modal',
            'RP': 'Particle',
            '$': 'Dollar Sign',
            'WRB': 'Wh-Adverb',
            'POS': 'Possessive Ending',
            'WP': 'Wh-Pronoun',
            'JJS': 'Adjective (superlative)',
            ':': 'Colon',
            'JJR': 'Adjective (comparative)',
            'RBR': 'Adverb (comparative)'
        };

        // extract top 5 pos data by count
        const top5PosCount = Object.entries(posCountData)
            .sort((a, b) => b[1] - a[1]) // Sort by count in descending order
            .slice(0, 5); // Get the top 5 entries

        // extract labels and counts
        const posLabels = top5PosCount.map(item => posTagNames[item[0]]);
        const posCounts = top5PosCount.map(item => item[1]);

        // instantiate POS tag chart
        var ctx_pos = document.getElementById('posChart_' + i).getContext('2d');
        var posChart = new Chart(ctx_pos, {
            type: 'bar',
            data: {
                labels: posLabels,
                datasets: [{
                    label: 'POS Tag Count',
                    data: posCounts,
                    backgroundColor: 'rgba(75, 192, 192, 0.2)', // Light green
                    borderColor: 'rgba(75, 192, 192, 1)',
                    borderWidth: 1
                }]
            },
            options: {
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
        // Finished drawing the pos tag chart
    }

    // simpletest
    // var element = document.getElementById("simpletest1");
    // var responseDataString = JSON.stringify(analysisResults, null, 2);
    // element.innerHTML = "<pre>" + responseDataString + "</pre>";


}

function pollForResult(selected_option, requestid) {
    var pollInterval = setInterval(function () {
        console.log('moshiur here!!!')
        console.log('Request ID:', requestid);
        // Poll backend endpoint to check status
        $.ajax({
            url: `/consumer/${selected_option}/${requestid}`,
            type: "GET",
            dataType: "json",  // Specify JSON data type
            success: function (data) {
                // Consume data from the JSON response
                var status = data.status;
                // var result = data.analysis_result;

                // Example: Update UI with result
                console.log("Status:", status);
                // console.log("Result:", result);

                if (status === "complete") {
                    // Processing complete, handle result
                    clearInterval(pollInterval);
                    // check the selected option and call the appropriate processing function
                    if (selected_option === "text_input") {
                        console.log('Did we get here?')
                        console.log(data)
                        processSingleInputDataTextInput(data.analysis_result);
                    } else if (selected_option === "files_input") {
                        console.log('Did we get here as files_input?')
                        console.log("data is: ", data)
                        processFilesInputData(data.analysis_results);
                    } else if (selected_option === "news_article_sources") {
                        console.log('Did we get here?')
                        console.log(data)
                        processSingleInputDataNewsArticle(data.analysis_result);
                    } else {
                        console.log("Error: Unsupported selected option.");
                    }
                } else if (status === "in_progress") {
                    // processing in progress, do something
                    console.log("Processing in progress...");
                } else {
                    // error or unknown status
                    console.log("Error or unknown status:", status);
                }
            },
            error: function (xhr, status, error) {
                // error handling
                console.error("Error:", error);
            }
        });
    }, 2000);
}


// Below for the {% elif selected_option == "files_input" %} case
// // Extracting data from Python dictionary for top 5 words
// const top5WordsData_{{ loop.index }} = {{ analysis_results[file_info.filename]['basic_text_analysis_dict'].top_n_words | tojson }};
//
// // Extracting words and frequencies
// const words_{{ loop.index }} = top5WordsData_{{ loop.index }}.map(item => item[0]);
// const frequencies_{{ loop.index }} = top5WordsData_{{ loop.index }}.map(item => item[1]);
//
// // Creating a new Chart instance for top 5 words
// var ctx_word_{{ loop.index }} = document.getElementById('wordChart_{{ loop.index }}').getContext('2d');
// var wordChart_{{ loop.index }} = new Chart(ctx_word_{{ loop.index }}, {
//     type: 'bar',
//     data: {
//         labels: words_{{ loop.index }},
//         datasets: [{
//             label: 'Word Frequency',
//             data: frequencies_{{ loop.index }},
//             backgroundColor: 'rgba(75, 192, 192, 0.2)', // Light green
//             borderColor: 'rgba(75, 192, 192, 1)',
//             borderWidth: 1
//         }]
//     },
//     options: {
//         scales: {
//             y: {
//                 beginAtZero: true
//             }
//         }
//     }
// });
//
// // Extracting data from Python dictionary for POS tag analysis
// const posCountData_{{ loop.index }} = {{ analysis_results[file_info.filename]['nlp_analysis_dict'].pos_count | tojson }};
//
// // Define a mapping of POS tags to their full names
// const posTagNames_{{ loop.index }} = {
//     'NN': 'Noun',
//     'DT': 'Determiner',
//     'NNP': 'Proper Noun',
//     'IN': 'Preposition or Subordinating Conjunction',
//     'NNS': 'Plural Noun',
//     'JJ': 'Adjective',
//     ',': 'Comma',
//     'PRP': 'Personal Pronoun',
//     'RB': 'Adverb',
//     'VB': 'Verb (base form)',
//     'VBD': 'Verb (past tense)',
//     'TO': 'to',
//     'VBP': 'Verb (non-3rd person singular present)',
//     '.': 'Period',
//     'VBG': 'Verb (gerund or present participle)',
//     'VBZ': 'Verb (3rd person singular present)',
//     'CC': 'Coordinating Conjunction',
//     "''": 'Closing quotation mark',
//     '``': 'Opening quotation mark',
//     'PRP$': 'Possessive Pronoun',
//     'CD': 'Cardinal Number',
//     'VBN': 'Verb (past participle)',
//     'WDT': 'Wh-Determiner',
//     'MD': 'Modal',
//     'RP': 'Particle',
//     '$': 'Dollar Sign',
//     'WRB': 'Wh-Adverb',
//     'POS': 'Possessive Ending',
//     'WP': 'Wh-Pronoun',
//     'JJS': 'Adjective (superlative)',
//     ':': 'Colon',
//     'JJR': 'Adjective (comparative)',
//     'RBR': 'Adverb (comparative)'
// };
//
// // Extracting top 5 POS tags and their counts
// const top5PosCount_{{ loop.index }} = Object.entries(posCountData_{{ loop.index }})
//     .sort((a, b) => b[1] - a[1]) // Sort by count in descending order
//     .slice(0, 5); // Get the top 5 entries
//
// // Extracting labels (POS names) and data (counts) for the chart
// const posLabels_{{ loop.index }} = top5PosCount_{{ loop.index }}.map(item => posTagNames_{{ loop.index }}[item[0]]);
// const posCounts_{{ loop.index }} = top5PosCount_{{ loop.index }}.map(item => item[1]);
//
// // Creating a new Chart instance for POS tag analysis
// var ctx_pos_{{ loop.index }} = document.getElementById('posChart_{{ loop.index }}').getContext('2d');
// var posChart_{{ loop.index }} = new Chart(ctx_pos_{{ loop.index }}, {
//     type: 'bar',
//     data: {
//         labels: posLabels_{{ loop.index }},
//         datasets: [{
//             label: 'POS Tag Count',
//             data: posCounts_{{ loop.index }},
//             backgroundColor: 'rgba(75, 192, 192, 0.2)', // Light green
//             borderColor: 'rgba(75, 192, 192, 1)',
//             borderWidth: 1
//         }]
//     },
//     options: {
//         scales: {
//             y: {
//                 beginAtZero: true
//             }
//         }
//     }
// });
//
// console.log("posCountData:", {{ analysis_results[file_info.filename]['nlp_analysis_dict'].pos_count | tojson }});
// // Debugging output for POS tag data
// console.log("posLabels_{{ loop.index }}:", posLabels_{{ loop.index }});
// console.log("posCounts_{{ loop.index }}:", posCounts_{{ loop.index }});


//------------------------------------------------------------------------------------------------------------------------
//     {% if selected_option != "files_input" %}
//     <script>
//         // Extracting data from Python dictionary
//         const topNWordsData = {{ analysis_result.basic_text_analysis_dict.top_n_words | tojson }};
//
//         // Extracting words and frequencies
//         const words = topNWordsData.map(item => item[0]);
//         const frequencies = topNWordsData.map(item => item[1]);
//
//         // Creating a new Chart instance
//         var ctx = document.getElementById('myChart').getContext('2d');
//         var myChart = new Chart(ctx, {
//             type: 'bar',
//             data: {
//                 labels: words,
//                 datasets: [{
//                     label: 'Word Frequency',
//                     data: frequencies,
//                     backgroundColor: 'rgba(75, 192, 192, 0.2)', // Light green
//                     borderColor: 'rgba(75, 192, 192, 1)',
//                     borderWidth: 1
//                 }]
//             },
//             options: {
//                 scales: {
//                     y: {
//                         beginAtZero: true
//                     }
//                 }
//             }
//         });
//     </script>
//     <script>
//         // Extracting data from Python dictionary
//         const posCountData = {{ analysis_result.nlp_analysis_dict.pos_count | tojson }};
//
//         // Define a mapping of POS tags to their full names
//         // https://stackoverflow.com/questions/15388831/what-are-all-possible-pos-tags-of-nltk
//         // https://www.ling.upenn.edu/courses/Fall_2003/ling001/penn_treebank_pos.html
//         const posTagNames = {
//             'NN': 'Noun',
//             'DT': 'Determiner',
//             'NNP': 'Proper Noun',
//             'IN': 'Preposition or Subordinating Conjunction',
//             'NNS': 'Plural Noun',
//             'JJ': 'Adjective',
//             ',': 'Comma',
//             'PRP': 'Personal Pronoun',
//             'RB': 'Adverb',
//             'VB': 'Verb (base form)',
//             'VBD': 'Verb (past tense)',
//             'TO': 'to',
//             'VBP': 'Verb (non-3rd person singular present)',
//             '.': 'Period',
//             'VBG': 'Verb (gerund or present participle)',
//             'VBZ': 'Verb (3rd person singular present)',
//             'CC': 'Coordinating Conjunction',
//             "''": 'Closing quotation mark',
//             '``': 'Opening quotation mark',
//             'PRP$': 'Possessive Pronoun',
//             'CD': 'Cardinal Number',
//             'VBN': 'Verb (past participle)',
//             'WDT': 'Wh-Determiner',
//             'MD': 'Modal',
//             'RP': 'Particle',
//             '$': 'Dollar Sign',
//             'WRB': 'Wh-Adverb',
//             'POS': 'Possessive Ending',
//             'WP': 'Wh-Pronoun',
//             'JJS': 'Adjective (superlative)',
//             ':': 'Colon',
//             'JJR': 'Adjective (comparative)',
//             'RBR': 'Adverb (comparative)'
//         };
//
//         // Extracting top 5 POS tags and their counts
//         const top5PosCount = Object.entries(posCountData)
//             .sort((a, b) => b[1] - a[1]) // Sort by count in descending order
//             .slice(0, 5); // Get the top 5 entries
//
//         // Extracting labels (POS names) and data (counts) for the chart
//         const posLabels = top5PosCount.map(item => posTagNames[item[0]]);
//         const posCounts = top5PosCount.map(item => item[1]);
//
//         // Creating a new Chart instance
//         var ctx = document.getElementById('posChart').getContext('2d');
//         var posChart = new Chart(ctx, {
//             type: 'bar',
//             data: {
//                 labels: posLabels,
//                 datasets: [{
//                     label: 'POS Tag Count',
//                     data: posCounts,
//                     backgroundColor: 'rgba(75, 192, 192, 0.2)', // Light green
//                     borderColor: 'rgba(75, 192, 192, 1)',
//                     borderWidth: 1
//                 }]
//             },
//             options: {
//                 scales: {
//                     y: {
//                         beginAtZero: true
//                     }
//                 }
//             }
//         });
//     </script>
// {% endif %}