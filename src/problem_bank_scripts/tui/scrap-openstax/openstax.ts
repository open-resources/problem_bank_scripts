import { CheerioAPI } from "cheerio";
import { range } from "lodash";
import { fetchScrap, sleep } from "./utils";
import { fixText } from "./fixText";
import { MathMLToLaTeX } from 'mathml-to-latex';

interface QuestionsSection { // may not be up to date
    variables: Record<string, string>;
    question_numbers: number[];
    title: string; // generate a title for the entire question
    parts: {
        solution: string;
        question: string;
        info: {
            type:
                | "multiple-choice"
                | "checkbox"
                | "number-input"
                | "longtext"
                | "dropdown"
                | "matrix"
                | "matching"
                | "true-false"
                | "yes-no"
                | "file-upload"
                | "integer-input"
                | "symbolic-input";
            choices?: { value: string; correct: boolean; feedback: string }[]; // for multiple-choice | checkbox | dropdown | yes-no | true-false
            digits: number; // for number-input
            label?: string; // for number-input | integer-input | symbolic-input (ex. "$p=$")
            suffix?: string; // for number-input
            code?: string; // python code to solve question as a string
            statements?: { value: string; matches: string }[]; // for matching
            options?: string[]; // for matching: generate around 2 extra statements with no matches. These should not overlap with those in "statements"
        };
    }[];
}

const tableElemToMatrix = ($: CheerioAPI, elem: any) => {
    // $.find
    const tables: string[][][] = [];
    $(elem)
        .find("table")
        .map((i, el) => {
            const header: string[] = [];
            $(el)
                .find("th")
                .map((i, th) => header.push($(th).text().trim()));
            const body: string[][] = [];
            $(el)
                .find("tbody tr")
                .map((i, tr) => {
                    const row: string[] = [];
                    $(tr)
                        .find("td")
                        .map(function () {
                            row.push($(this).text().trim());
                        });
                    body.push(row);
                });
            tables.push([header, ...body]);
        });
    return tables.map((table) => table.map((row) => row.map(fixText)));
};

interface Question {
    questionNumber: number;
    questionText: string;
    tables?: string[][][];
    parts: string[];
}

function removeQuestionNumber(text: string): string {
    // Regular expression to match question number with optional whitespace and newlines
    const regex = /^\d+\.\s*\n\n/;

    // Replace the matched string with an empty string
    return text.replace(regex, "").trim();
}

export async function scrapOpenstax(
    url = "https://openstax.org/books/introductory-statistics-2e/pages"
) {
    // const chapters = range(8, 8 + 1);
    const chapters = range(1, 13 + 1);

    const sections = [
        "practice",
        "bringing-it-together-practice",
        "homework",
        "bringing-it-together-homework",
    ];
    const questionGroups: Record<
        number,
        {
            description: string;
            parts: Question[];
            sectionHref: string;
            tables?: string[][][];
        }[]
    > = {};
    const solutions: Record<
        number,
        Record<
            number,
            { tables?: string[][][]; images?: string[]; parts: string[] } // TODO: removed questionText from solutions
        >
    > = {};
    for (let c of chapters) {
        questionGroups[c] = [];
        let currentSectionHref = ""; // can go across pages
        for (let i = 0; i < sections.length; i++) {
            let section = sections[i];
            solutions[c] = {};
            sleep(1000);
            const $ = await fetchScrap(`${url}/${c}-${section}`);
            let currentGroupInfo: Record<string, any> = {
                descriptionHTML: [],
            };
            let questions: Question[] = [];
            let tables: string[][][] = [];
            $(`main #main-content section[data-depth="1"]`)
                .children()
                .each((i, elem) => {
                    if ($(elem).is("a")) {
                        currentSectionHref = elem.attribs.href;
                    } else if ($(elem).is("div.os-figure")) {
                        currentGroupInfo.descriptionHTML.push(
                            $(elem).find("img").toString()
                        );
                        $(elem).find("img").remove();
                    } else if ($(elem).is(".os-table")) {
                        const matrices = tableElemToMatrix($, elem);
                        currentGroupInfo.descriptionHTML.push(
                            "{{{ params.TABLE_GOES_HERE }}}"
                        );
                        tables = tables.concat(matrices);
                    } else if (
                        $(elem).is("p") ||
                        $(elem).is('[data-type="note"]')
                    ) {
                        const description = $(elem)
                            .contents()
                            .filter(function () {
                                return (
                                    this.type !== "tag" || this.tagName !== "em"
                                );
                            })
                            .text()
                            .trim();
                        currentGroupInfo.descriptionHTML.push(description);
                    } else if ($(elem).is('[data-type="exercise"]')) {
                        const questionNumber = $(elem)
                            .find("span.os-number, a.os-number")
                            .first()
                            .text()
                            .trim();

                        for (const child of $(elem).find("section")[0]
                            .children) {
                            if (child.type === "comment") {
                                if (!(parseInt(questionNumber) in solutions[c]))
                                    solutions[c][parseInt(questionNumber)] = {
                                        parts: [],
                                    };
                                solutions[c][
                                    parseInt(questionNumber)
                                ].parts.push(child.data);
                            }
                        }

                        $(elem).find(
                            `div[data-type="problem"] div.os-problem-container`
                        );

                        let { description: questionText, tables: partTables } =
                            getProblemDescription($, elem);

                        const imageString = $(elem).find("img").toString();
                        if (imageString) questionText += "\n" + imageString;

                        const parts = recursiveHandleProblemElements(
                            $(elem)
                                .find(
                                    `div[data-type="problem"] div.os-problem-container ol`
                                )
                                .first(),
                            $,
                            partTables
                        );
                        if (parts.length === 0 && questionText.trim()) {
                            parts.push("");
                        }

                        questions.push({
                            questionNumber: parseInt(questionNumber),
                            questionText,
                            ...(partTables.length > 0 && {
                                tables: partTables,
                            }),
                            parts,
                        });

                        // Check the next sibling to decide if we should end the current group
                        const nextElem = $(elem).next();
                        if (!nextElem.is('[data-type="exercise"]')) {
                            // If the next element is not a <div>, end the current group
                            questionGroups[c].push({
                                description: fixText(
                                    currentGroupInfo.descriptionHTML.join("\n")
                                ),
                                parts: questions,
                                sectionHref: url + "/" + currentSectionHref,
                                ...(tables.length > 0 && { tables }),
                            });
                            currentGroupInfo = {
                                descriptionHTML: [],
                            };
                            questions = [];
                            tables = [];
                        }
                    } else {
                        console.log(
                            elem.type,
                            elem.tagName,
                            elem.attribs,
                            currentSectionHref
                        );
                        currentGroupInfo.descriptionHTML.push(
                            $(elem).toString()
                        );
                    }
                });

            if (questions.length > 0) {
                questionGroups[c].push({
                    description: currentGroupInfo.descriptionHTML.join("\n"),
                    parts: questions,
                    sectionHref: url + "/" + currentSectionHref,
                    ...(tables.length > 0 && { tables }),
                });
            }
        }
        const $ = await fetchScrap(`${url}/${c}-solutions`);
        $(`main .os-solutions-container div[data-type="solution"]`).map(
            (i, elem) => {
                const questionNumber = parseInt(
                    $(elem).find("a.os-number").first().text().trim()
                );
                if (isNaN(questionNumber)) return;

                const tables = tableElemToMatrix($, elem);
                $(elem).find("table").remove();

                const questionText = removeQuestionNumber(
                    $(elem).text().trim()
                );

                const parts = recursiveHandleProblemElements(
                    $(elem).find(`div.os-solution-container ol`).first(),
                    $,
                    tables
                );

                const imageStrings: string[] = [];
                $(elem)
                    .find("img")
                    .map((i, el) => imageStrings.push($(el).toString()));
                solutions[c][questionNumber] = {
                    parts,
                    ...(tables.length && { tables }),
                    ...(imageStrings.length && { images: imageStrings }),
                };
            }
        );
    }
    writeJson({ questions: questionGroups, solutions }, "questions.json");
}

function writeJson(data: object, filename: string = "./saved.json"): void {
    const fs = require("fs"); // Import the 'fs' module for file system access

    try {
        const jsonData = JSON.stringify(data, null, 4); // Stringify with indentation
        fs.writeFileSync(filename, jsonData, { encoding: "utf8" }); // Write with UTF-8 encoding
    } catch (error) {
        console.error("Error writing JSON file:", error);
    }
}

const ulToMarkdown = ($: CheerioAPI, elem: any, tables: string[][][]) => {
    let text = "";
    let parts: string[] = [];
    $(elem)
        .children()
        .each((i, node) => {
            if (node.tagName !== "li")
                throw new Error(
                    "Expected <li> tag in <ul>, got " + node.tagName
                );
            parts = parts.concat(
                handleWithinLi($, node, tables, {
                    squashNested: false,
                    markdownStyle: true,
                })
            );
        });

    if (text && parts.length > 0) {
        text = text + "\n";
    }

    return text + parts.map((part) => fixText(part)).join(`\n-`);
};

function getProblemDescription($: CheerioAPI, elem: any) {
    let description = "";
    let tables: string[][][] = [];
    $(elem)
        .find(`div[data-type="problem"] div.os-problem-container`)
        .children()
        .each((i, elem) => {
            if ($(elem).is("p") || $(elem).is('[data-type="note"]')) {
                description += fixText($(elem).text());
            } else if ($(elem).is("ol")) {
                return;
            } else if ($(elem).is("div.os-figure")) {
                description += "\n" + $(elem).find("img").toString();
                $(elem).find("img").remove();
            } else if ($(elem).is(".os-table")) {
                const matrices = tableElemToMatrix($, elem);
                description += "\n{{{ params.TABLE_GOES_HERE }}}";
                tables = tables.concat(matrices);
            } else if (elem.tagName === "strong") {
                description += fixText("**" + $(elem).text() + "**");
            } else if (elem.tagName === "ul") {
                description += ulToMarkdown($, elem, tables);
            } else if (elem.tagName === "div") {
                console.log(
                    "Div in description:",
                    elem.type,
                    elem.attribs,
                    $(elem).text()
                );
                description += fixText($(elem).text());
            } else {
                console.log(
                    "Unknown element in description:",
                    elem.type,
                    elem.tagName,
                    elem.attribs,
                    $(elem).text()
                );
                elem.attribs = {};
                description += fixText($(elem).toString());
            }
        });
    return { description: fixText(description), tables };
}

function handleWithinLi(
    $: CheerioAPI,
    elem: any,
    tables: string[][][],
    { squashNested = true, markdownStyle = false } = {}
) {
    let parts: string[] = [];
    let part = "";
    $(elem)
        .contents()
        .each((index, node) => {
            if (node.type === "text") {
                const textContent = $(node).text().trim();
                if (textContent) {
                    part += "\n" + textContent;
                }
            } else if (node.type === "tag") {
                const tagName = $(node).prop("tagName").toLowerCase();
                if (tagName === "ol" || tagName === "ul") {
                    // to handle
                    const newParts = recursiveHandleProblemElements(
                        node,
                        $,
                        tables
                    );
                    if (part) {
                        newParts[0] = `For the following ${
                            newParts.length
                        } questions: ${part.trim()}\n${newParts[0].trim()}`;
                        part = "";
                    }
                    if (!squashNested) {
                        if (markdownStyle) {
                            part +=
                                "\n" +
                                newParts.join(
                                    tagName === "ul" ? "\n- " : "1. "
                                );
                        } else
                            throw new Error(
                                `Nested <${tagName}> not supported`
                            );
                    } else {
                        parts = parts.concat(newParts);
                    }
                } else if (tagName === "math") {
                    const latex = MathMLToLaTeX.convert($(node).toString());
                    part += " " + latex.trim();
                } else if (
                    tagName === "p" ||
                    tagName === "span" ||
                    $(node).is('[data-type="note"]')
                ) {
                    part += "\n" + fixText($(node).text());
                } else if ($(node).is(".os-table")) {
                    // not a new part, only <li> is a new part
                    const matrices = tableElemToMatrix($, node);
                    part += "\n{{{ params.TABLE_GOES_HERE }}}";
                    for (const m of matrices) {
                        tables.push(m);
                    }
                } else if ($(node).is("div.os-figure")) {
                    part += "\n" + $(node).find("img").toString();
                    $(node).find("img").remove();
                } else if (tagName === "em") {
                    part += fixText("$" + $(node).text() + "$");
                } else if (tagName === "sub") {

                    part += "$_" + $(node).text() + "$";
                    part = fixText(part);
                } else if (tagName === "sup") {
                    part += "$^" + $(node).text() + "$";
                    part = fixText(part);
                } else if (tagName === "strong") {
                    part += fixText("**" + $(node).text() + "**");
                } else if (tagName === "a") {
                    const href = $(node).attr("href");
                    if (href?.startsWith("http")) {
                        part += fixText(
                            `[${$(node).text()}](${$(node).attr("href")})`
                        );
                    }
                } else {
                    console.log(
                        "Unknown element in <li>:",
                        node.type,
                        node.tagName,
                        node.attribs,
                        fixText($(node).text())
                    );
                    node.attribs = {};
                    part += fixText($(node).toString());
                }
            } else {
                // TODO: this could be comments?
                console.log(
                    "Unknown node.type:",
                    node.type,
                    fixText($(node).text())
                );
                throw new Error(
                    "Unknown node type in <li> of handleProblemElements"
                );
            }
        });
    if (parts.length > 0) {
        if (part) parts.push(part);
        return parts.map((part) => fixText(part));
    }
    return [fixText(part)];
}

function recursiveHandleProblemElements(
    parentElem: any,
    $: CheerioAPI,
    partTables: string[][][]
): string[] {
    let parts: string[] = [];
    $(parentElem)
        .children()
        .each((i, elem) => {
            if ($(elem).is("ol")) {
                $(elem)
                    .children()
                    .each((i, elem) => {
                        const newParts = recursiveHandleProblemElements(
                            elem,
                            $,
                            partTables
                        );
                        parts = parts.concat(newParts);
                    });
            } else if ($(elem).is("li")) {
                // parts.push($(elem).text().trim());
                parts = parts.concat(handleWithinLi($, elem, partTables));
            } else {
                parts.push(fixText($(elem).toString()));
                console.log(
                    "Unknown element:",
                    elem.type,
                    elem.tagName,
                    elem.attribs,
                    fixText($(elem).text())
                );
            }
        });
    return parts.map((part) => fixText(part));
}
