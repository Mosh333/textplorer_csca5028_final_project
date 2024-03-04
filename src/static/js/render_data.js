// render_data.js

function processSingleInputData(analysisResult) {
    const topNWordsData = analysisResult.basic_text_analysis_dict.top_n_words;
    const words = topNWordsData.map(item => item[0]);
    const frequencies = topNWordsData.map(item => item[1]);

    // Show the analysis result elements
    document.getElementById('analysis-results').style.display = 'block';
    document.getElementById('loading-message').remove();

    // Basic Text Analysis
    const basicTextAnalysisDict = analysisResult.basic_text_analysis_dict;
    const basicTextAnalysisContainer = document.getElementById('basic-text-analysis-container');
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
    const sentimentAnalysisContainer = document.getElementById('sentiment-analysis-container');
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
    const nlpAnalysisContainer = document.getElementById('nlp-analysis-container');
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
    var ctxWord = document.getElementById('myChart').getContext('2d');
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

    var ctxPos = document.getElementById('posChart').getContext('2d');
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

function processFilesInputData(analysis_results, file_info, loop_index) {
    // Extracting data from Python dictionary for top 5 words
    const top5WordsData = analysis_results[file_info.filename]['basic_text_analysis_dict'].top_n_words;

    // Extracting words and frequencies
    const words = top5WordsData.map(item => item[0]);
    const frequencies = top5WordsData.map(item => item[1]);

    // Creating a new Chart instance for top 5 words
    var ctx_word = document.getElementById('wordChart_' + loop_index).getContext('2d');
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

    // Extracting data from Python dictionary for POS tag analysis
    const posCountData = analysis_results[file_info.filename]['nlp_analysis_dict'].pos_count;

    // Define a mapping of POS tags to their full names
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

    // Extracting top 5 POS tags and their counts
    const top5PosCount = Object.entries(posCountData)
        .sort((a, b) => b[1] - a[1]) // Sort by count in descending order
        .slice(0, 5); // Get the top 5 entries

    // Extracting labels (POS names) and data (counts) for the chart
    const posLabels = top5PosCount.map(item => posTagNames[item[0]]);
    const posCounts = top5PosCount.map(item => item[1]);

    // Creating a new Chart instance for POS tag analysis
    var ctx_pos = document.getElementById('posChart_' + loop_index).getContext('2d');
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

    console.log("posCountData:", posCountData);
    // Debugging output for POS tag data
    console.log("posLabels_" + loop_index + ":", posLabels);
    console.log("posCounts_" + loop_index + ":", posCounts);
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
                    // Check the selected option and call the appropriate processing function
                    if (selected_option === "text_input") {
                        console.log('Did we get here?')
                        console.log(data)
                        processSingleInputData(data.analysis_result);
                    } else if (selected_option === "files_input") {
                        processFilesInputData(data.analysis_results, data.file_info, data.loop_index);
                    } else if (selected_option === "news_article_sources") {
                        processSingleInputData(result.analysis_result);
                    } else {
                        console.log("Error: Unsupported selected option.");
                    }
                } else if (status === "in_progress") {
                    // Processing in progress, do something
                    console.log("Processing in progress...");
                } else {
                    // Error or unknown status, handle accordingly
                    console.log("Error or unknown status:", status);
                }
            },
            error: function (xhr, status, error) {
                // Error handling
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